"""
Script to calculate the risk of slashing penalties for Lido validators
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm

from environ.constants import SAMPLE_DATA_DICT
from environ.fetch.block import date_close_to_block
from environ.fetch.lido import Lido
from environ.fetch.w3 import w3
from environ.process.risk_slashing import (
    EFFECTIVE_BALANCE_INCREMENT,
    MAX_EFFECTIVE_BALANCE,
    MAX_VALIDATOR_COUNT,
    get_epoch_data,
    get_exam_slashing,
    gwei_to_ether,
)

lido = Lido(w3)
EVENT_TO_SLOT = {"max_tvl": 87871, "luna_collapse": 118012, "ftx_collapse": 159187}
EVENT_TO_UPDATE = {
    "max_tvl": "Altair",
    "luna_collapse": "Bellatrix",
    "ftx_collapse": "Bellatrix",
}
EVENT_TO_NODE_OPERATOR = {"max_tvl": 5265, "luna_collapse": 7391, "ftx_collapse": 7391}

result_dict = {}

for event, date in SAMPLE_DATA_DICT.items():
    result_dict[event] = {}
    for num_node_operator in tqdm(range(1, 4, 1)):
        # current state of beacon chain
        current_epoch_data = get_epoch_data(EVENT_TO_SLOT[event])
        validatorscount_current = int(current_epoch_data["validatorscount"])
        current_epoch = current_epoch_data["epoch"]
        totalvalidatorbalance_current = current_epoch_data["totalvalidatorbalance"]
        eligibleether_current = current_epoch_data["eligibleether"]
        avarage_effective_balance = eligibleether_current / validatorscount_current
        validatorscount_current_param = (
            validatorscount_current * 1.05 - validatorscount_current * 1.05 % 10000
        )

        # Lido param
        current_lido_deposits = lido.get_total_pooled_ether(date_close_to_block(date))

        current_lido_treasury = (
            10.154232576699999999 * 365 * 5
        )  # 5 year Lido earnings at current rate
        future_lido_treasury = (
            10.154232576699999999 * 365 * 5
        )  # 5 year Lido earnings at current rate
        future_lido_share = 0.25
        current_lido_validator_average_eff_balance = MAX_EFFECTIVE_BALANCE
        current_lido_validator_average_balance = 33000000000
        future_lido_validator_average_eff_balance = MAX_EFFECTIVE_BALANCE
        future_lido_validator_average_balance = 33000000000
        current_biggest_node_operator = EVENT_TO_NODE_OPERATOR[event]
        future_biggest_node_operator = 10000
        period_offline = 256  # epochs

        # params for calculation
        validatorscount = np.array(
            [validatorscount_current_param, MAX_VALIDATOR_COUNT]
        )  # validatorscount_current_param*10])#MAX_VALIDATOR_COUNT])
        eligibleether = validatorscount * (gwei_to_ether(avarage_effective_balance))
        lidoshare = [
            current_lido_deposits / gwei_to_ether(current_epoch_data["eligibleether"]),
            future_lido_share,
        ]
        lidotreasury = [current_lido_treasury, future_lido_treasury]
        lidostakeddeposits = [
            eligibleether[x] * lidoshare[x] for x in range(len(lidoshare))
        ]
        lidoavgeffbalance = gwei_to_ether(
            np.array(
                [
                    current_lido_validator_average_eff_balance,
                    future_lido_validator_average_eff_balance,
                ]
            )
        )
        lidoavgbalance = gwei_to_ether(
            np.array(
                [
                    current_lido_validator_average_balance,
                    future_lido_validator_average_balance,
                ]
            )
        )
        lidobigoperator = [
            [current_biggest_node_operator, current_biggest_node_operator],
            [future_biggest_node_operator, future_biggest_node_operator],
        ]

        state = "current"
        spec = EVENT_TO_UPDATE[event]

        if state == "future":
            state_dummy = 1
        else:
            state_dummy = 0
            exams = [
                [
                    x * 0.01 * lidobigoperator[0][0] * num_node_operator,
                    x * 0.01 * lidobigoperator[1][0] * num_node_operator,
                ]
                for x in range(0, 101, 1)
            ]

            inputdata = {
                "total active validators": validatorscount,
                "total eligible ETH": eligibleether,
                "Lido's share": lidoshare,
                "Lido's deposits": lidostakeddeposits,
                "5y_earnings": lidotreasury,
                "avarage effective balance of Lido's validators": lidoavgeffbalance,
                "avarage balance of Lido's validators": lidoavgbalance,
                **{
                    f"single big operator, {x}% validators offline/slashed": exams[x]
                    for x in range(0, 101, 1)
                },
            }

            lidoavgbalance = (
                inputdata.get("avarage balance of Lido's validators")[state_dummy]
                * EFFECTIVE_BALANCE_INCREMENT
            )
            lidoavgeffbalance = (
                inputdata.get("avarage effective balance of Lido's validators")[
                    state_dummy
                ]
                * EFFECTIVE_BALANCE_INCREMENT
            )
            validatorscount = inputdata.get("total active validators")[state_dummy]
            avarage_effective_balance = (
                inputdata.get("total eligible ETH")[state_dummy]
                * EFFECTIVE_BALANCE_INCREMENT
                / validatorscount
            )
            lidostakeddeposits = (
                inputdata.get("Lido's deposits")[state_dummy]
                * EFFECTIVE_BALANCE_INCREMENT
            )
            lidotreasury = (
                inputdata.get("5y_earnings")[state_dummy] * EFFECTIVE_BALANCE_INCREMENT
            )

            result_list = [
                get_exam_slashing(
                    exams[y][state_dummy],
                    lidoavgbalance,
                    lidoavgeffbalance,
                    validatorscount,
                    avarage_effective_balance,
                    spec,
                )
                for y in range(len(exams))
            ]

            df_result = pd.DataFrame(
                result_list,
                index=[
                    f"single big operator, {x}% validators slashed"
                    for x in range(0, 101, 1)
                ],
            )
            df_result["%_of_lido_deposits"] = df_result.total_loss / gwei_to_ether(
                lidostakeddeposits
            )
            df_result["%_of_5y_earnings"] = df_result.total_loss / gwei_to_ether(
                lidotreasury
            )

            # print(df_result[["total_loss", "%_of_lido_deposits", "%_of_5y_earnings"]])
            plt.plot(range(0, 101, 1), df_result.total_loss)

            result_dict[event][num_node_operator] = {
                "slashing": range(0, 101, 1),
                "loss": df_result["%_of_lido_deposits"].values.tolist(),
            }
    print(validatorscount_current)
