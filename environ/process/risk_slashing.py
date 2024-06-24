"""
Function to calculate the risk of slashing for a validator
"""
import logging
import math

import numpy as np
import pandas as pd
import requests

pd.options.display.float_format = "{:,.2f}".format


SLOTS_PER_EPOCH = 32
BASE_REWARDS_PER_EPOCH = 4
BASE_REWARD_FACTOR = 2**6
MAX_EFFECTIVE_BALANCE = 2**5 * 10**9
EFFECTIVE_BALANCE_INCREMENT = 2**0 * 10**9
EPOCHS_PER_SLASHING = 2**13  # ~36 days or 8192 epochs

MIN_SLASHING_PENALTY_QUOTIENT = 2**7
MIN_SLASHING_PENALTY_QUOTIENT_ALTAIR = 2**6  # (= 64)
MIN_SLASHING_PENALLTY_QUOTIENT_BELLATRIX = 2**5  # (= 32)

PROPORTIONAL_SLASHING_MULTIPLIER = 1
PROPORTIONAL_SLASHING_MULTIPLIER_ALTAIR = 2
PROPORTIONAL_SLASHING_MULTIPLIER_BELLATRIX = 3

TIMELY_SOURCE_WEIGHT = 14
TIMELY_TARGET_WEIGHT = 26
TIMELY_HEAD_WEIGHT = 14
SYNC_REWARD_WEIGHT = 2
PROPOSER_WEIGHT = 8
WEIGHT_DENOMINATOR = 64
SYNC_COMMITTEE_SIZE = 2**9  # (= 512)	Validators
EPOCHS_PER_SYNC_COMMITTEE_PERIOD = 2**8  # (= 256)	epochs	~27 hours
HYSTERESIS_QUOTIENT = 4
HYSTERESIS_DOWNWARD_MULTIPLIER = 1
HYSTERESIS_UPWARD_MULTIPLIER = 5
HYSTERESIS_INCREMENT = EFFECTIVE_BALANCE_INCREMENT // HYSTERESIS_QUOTIENT
DOWNWARD_THRESHOLD = HYSTERESIS_INCREMENT * HYSTERESIS_DOWNWARD_MULTIPLIER
UPWARD_THRESHOLD = HYSTERESIS_INCREMENT * HYSTERESIS_UPWARD_MULTIPLIER
MAX_VALIDATOR_COUNT = 2**19  # (= 524,288)


## Get current beacon chain data


def get_epoch_data(epoch: str|int = "latest") -> dict:
    """
    Function to get the current epoch data from the beacon chain
    """
    try:
        req = requests.get(
            f"https://beaconcha.in/api/v1/epoch/{epoch}",
            headers={"accept": "application/json"},
            timeout=60,
        )
        req.raise_for_status()
        return req.json()["data"]
    except requests.exceptions.HTTPError as err:
        logging.error(err)
        return {}


## Get aggregated results


def get_results_offline(exams: dict, inputdata: dict, epochs_offline: int) -> None:
    """
    Function to get the aggregated results for offline penalties
    """
    states = ["current", "future"]
    specs = ["Phase 0", "Altair"]
    results = [
        get_result_offline(epochs_offline, exams, inputdata, state, spec)
        for spec in specs
        for state in states
    ]
    titles = [(state, spec) for spec in specs for state in states]
    for result in range(len(results)):
        pd.options.display.float_format = "{:,.2f}".format
        display(titles[result], str(epochs_offline) + " epochs_offline")
        display(results[result])
        print()
    # return results


def get_results_slashing(exams: dict, inputdata: dict) -> None:
    """
    Function to get the aggregated results for slashing penalties
    """
    states = ["current", "future"]
    specs = ["Phase 0", "Altair"]
    results = [
        get_result_slashing(exams, inputdata, state, spec)
        for spec in specs
        for state in states
    ]
    titles = [(state, spec) for spec in specs for state in states]
    for result in range(len(results)):
        pd.options.display.float_format = "{:,.2f}".format
        display(titles[result])
        display(results[result])
        print()
    # return results


## Get result for a given state (current, future) and spec (Phase 0, Altair)


def get_result_offline(
    epochs_offline: int, exams: dict, inputdata: dict, state: str, spec: str
) -> pd.DataFrame:
    """
    Function to get the result for offline penalties
    """

    if state == "future":
        x = 1
    else:
        x = 0

    lidoavgbalance = (
        inputdata.get("avarage balance of Lido's validators")[x]
        * EFFECTIVE_BALANCE_INCREMENT
    )
    lidoavgeffbalance = (
        inputdata.get("avarage effective balance of Lido's validators")[x]
        * EFFECTIVE_BALANCE_INCREMENT
    )
    validatorscount = inputdata.get("total active validators")[x]
    avarage_effective_balance = (
        inputdata.get("total eligible ETH")[x]
        * EFFECTIVE_BALANCE_INCREMENT
        / validatorscount
    )
    lidostakeddeposits = (
        inputdata.get("Lido's deposits")[x] * EFFECTIVE_BALANCE_INCREMENT
    )
    lidotreasury = inputdata.get("5y_earnings")[x] * EFFECTIVE_BALANCE_INCREMENT

    result_list = [
        get_exam_offline(
            epochs_offline,
            exams[y][x],
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
            "single big operator, 30% validators offline",
            "single big operator, 100% validators offline",
            "two big operators, 30% validators offline",
            "two big operators, 100% validators offline",
        ],
    )
    df_result["%_of_lido_deposits"] = df_result.total_loss / gwei_to_ether(
        lidostakeddeposits
    )
    df_result["%_of_5y_earnings"] = df_result.total_loss / gwei_to_ether(lidotreasury)
    return df_result[["total_loss", "%_of_lido_deposits", "%_of_5y_earnings"]]


def get_result_slashing(
    exams: dict, inputdata: dict, state: str, spec: str
) -> pd.DataFrame:
    """
    Function to get the result for slashing penalties
    """

    if state == "future":
        x = 1
    else:
        x = 0

    lidoavgbalance = (
        inputdata.get("avarage balance of Lido's validators")[x]
        * EFFECTIVE_BALANCE_INCREMENT
    )
    lidoavgeffbalance = (
        inputdata.get("avarage effective balance of Lido's validators")[x]
        * EFFECTIVE_BALANCE_INCREMENT
    )
    validatorscount = inputdata.get("total active validators")[x]
    avarage_effective_balance = (
        inputdata.get("total eligible ETH")[x]
        * EFFECTIVE_BALANCE_INCREMENT
        / validatorscount
    )
    lidostakeddeposits = (
        inputdata.get("Lido's deposits")[x] * EFFECTIVE_BALANCE_INCREMENT
    )
    lidotreasury = inputdata.get("5y_earnings")[x] * EFFECTIVE_BALANCE_INCREMENT

    result_list = [
        get_exam_slashing(
            exams[y][x],
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
            "single big operator, 30% validators slashed",
            "single big operator, 100% validators slashed",
            "two big operators, 30% validators slashed",
            "two big operators, 100% validators slashed",
        ],
    )
    df_result["%_of_lido_deposits"] = df_result.total_loss / gwei_to_ether(
        lidostakeddeposits
    )
    df_result["%_of_5y_earnings"] = df_result.total_loss / gwei_to_ether(lidotreasury)
    return df_result[["total_loss", "%_of_lido_deposits", "%_of_5y_earnings"]]


## Get result for a given exam


def get_exam_offline(
    epochs_offline: int,
    exam: int,
    lidoavgbalance: int,
    lidoavgeffbalance: int,
    validatorscount: int,
    avarage_effective_balance: int,
    spec: str,
):
    """
    Function to get the result for offline penalties from a given exam
    """
    dic = {}

    match spec:
        case "Altair":
            result = process_offline_validator_altair(
            epochs_offline,
            lidoavgbalance,
            lidoavgeffbalance,
            validatorscount,
            avarage_effective_balance,
        )         
        case "Phase 0":
            result = process_offline_validator(
                epochs_offline,
                lidoavgbalance,
                lidoavgeffbalance,
                validatorscount,
                avarage_effective_balance,
            )

    prob_number_validators_assigned = (
        get_probability_outcomes(exam, validatorscount) * result[4]
    )
    dic.update({"offline_count": exam})
    dic.update(
        {
            "total_loss_offline_penalty": gwei_to_ether(
                (result[0] - lidoavgbalance) * exam
            )
        }
    )
    dic.update(
        {"average_loss_offline_penalty": gwei_to_ether(result[0] - lidoavgbalance)}
    )
    dic.update(
        {
            "total_loss": gwei_to_ether(
                (result[0] - lidoavgbalance) * (exam - prob_number_validators_assigned)
                + (result[2] - lidoavgbalance) * prob_number_validators_assigned
            )
        }
    )
    dic.update({"average_loss": gwei_to_ether(result[2] - lidoavgbalance)})
    return dic


def get_exam_slashing(
    exam: int,
    lidoavgbalance: int,
    lidoavgeffbalance: int,
    validatorscount: int,
    avarage_effective_balance: int,
    spec: str,
):
    """
    Function to get the result for slashing penalties from a given exam
    """
    dic = {}
    match spec:
        case "Altair" | "Bellatrix":
            result = process_slashings_altair_belltrix(
                exam,
                lidoavgbalance,
                lidoavgeffbalance,
                validatorscount,
                avarage_effective_balance,
                is_altair=(
                    spec == "Altair"
                ),
            )
        case "Phase 0":
            result = process_slashings(
                exam,
                lidoavgbalance,
                lidoavgeffbalance,
                validatorscount,
                avarage_effective_balance,
            )

    dic.update({"slashings_count": exam})
    dic.update({"total_loss": gwei_to_ether((result[0] - lidoavgbalance) * exam)})
    dic.update({"average_loss": gwei_to_ether(result[0] - lidoavgbalance)})
    return dic


## Offline penalties calculation Phase 0


def process_offline_validator(
    epochs_offline: int,
    lidoavgbalance: int,
    lidoavgeffbalance: int,
    validatorscount: int,
    avarage_effective_balance: int,
) -> tuple:
    """
    Function to calculate the offline penalties for a given number of epochs
    """
    balance = lidoavgbalance
    effective_balance = lidoavgeffbalance
    total_active_balances = (validatorscount) * avarage_effective_balance
    epoch = 0
    while epoch <= epochs_offline:
        balance, effective_balance = process_offline_penalty(
            balance, effective_balance, total_active_balances
        )
        epoch += 1
    return balance, effective_balance, balance, effective_balance, 0


## Offline penalties calculation Altair


def process_offline_validator_altair(
    epochs_offline: int,
    lidoavgbalance: int,
    lidoavgeffbalance: int,
    validatorscount: int,
    avarage_effective_balance: int,
) -> tuple:
    """
    Function to calculate the offline penalties for a given number of epochs
    """
    sync_comittees = math.ceil(epochs_offline / EPOCHS_PER_SYNC_COMMITTEE_PERIOD)
    sync_penalty_period = sync_comittees * EPOCHS_PER_SYNC_COMMITTEE_PERIOD
    balance = lidoavgbalance
    balance_sync = lidoavgbalance
    effective_balance = lidoavgeffbalance
    effective_balance_sync = lidoavgeffbalance
    total_active_balances = (validatorscount) * avarage_effective_balance
    epoch = 0
    while epoch <= epochs_offline:
        balance, effective_balance = process_offline_penalty_altair_bellatrix(
            balance, effective_balance, total_active_balances
        )
        balance_sync, effective_balance_sync = process_offline_penalty_altair_bellatrix(
            balance_sync, effective_balance_sync, total_active_balances
        )
        balance_sync, effective_balance_sync = process_sync_penalty_altair(
            balance_sync, effective_balance_sync, total_active_balances
        )
        epoch += 1
    if epochs_offline < sync_penalty_period:
        while epoch <= sync_penalty_period:
            balance_sync, effective_balance_sync = process_sync_penalty_altair(
                balance_sync, effective_balance_sync, total_active_balances
            )
            epoch += 1

    return (
        balance,
        effective_balance,
        balance_sync,
        effective_balance_sync,
        sync_comittees,
    )


## Slashing penalties calculation Phase 0


def process_slashings(
    slashed_validator_cnt: int,
    lidoavgbalance: float,
    lidoavgeffbalance: float,
    validatorscount: int,
    avarage_effective_balance: float,
) -> tuple:
    """
    Function to get aggreate results of slashing at Phase 0
    """

    balance = lidoavgbalance
    effective_balance = lidoavgeffbalance
    total_active_balances = (
        validatorscount - slashed_validator_cnt
    ) * avarage_effective_balance
    slashed_validator_balance = effective_balance * slashed_validator_cnt

    # initial_penalty
    balance, effective_balance = process_initial_penalty(balance, effective_balance)

    # offline_penalty
    exiting_epoch = 0
    while exiting_epoch <= EPOCHS_PER_SLASHING // 2:
        balance, effective_balance = process_offline_penalty(
            balance, effective_balance, total_active_balances
        )
        exiting_epoch += 1

    # special_penalty
    balance, effective_balance = process_special_penalty(
        balance, effective_balance, total_active_balances, slashed_validator_balance
    )

    # offline_penalty
    while exiting_epoch <= EPOCHS_PER_SLASHING:
        balance, effective_balance = process_offline_penalty(
            balance, effective_balance, total_active_balances
        )
        exiting_epoch += 1

    return balance, effective_balance


## Slashing penalties calculation Altair


def process_slashings_altair_belltrix(
    slashed_validator_cnt: int,
    lidoavgbalance: int,
    lidoavgeffbalance: int,
    validatorscount: int,
    avarage_effective_balance: int,
    is_altair: bool
) -> tuple:
    """
    Function to calculate the slashing penalties for a given number of slashed validators at Altair
    """

    balance = lidoavgbalance
    effective_balance = lidoavgeffbalance
    total_active_balances = (
        validatorscount - slashed_validator_cnt
    ) * avarage_effective_balance
    slashed_validator_balance = effective_balance * slashed_validator_cnt

    # initial_penalty
    balance, effective_balance = process_initial_penalty_altair_bellatrix(
        balance, effective_balance, is_altair
    )

    # exiting_penalty
    exiting_epoch = 0
    while exiting_epoch <= EPOCHS_PER_SLASHING // 2:
        balance, effective_balance = process_offline_penalty_altair_bellatrix(
            balance, effective_balance, total_active_balances
        )
        exiting_epoch += 1

    # special_penalty
    balance, effective_balance = process_special_penalty_altair_bellatrix(
        balance, effective_balance, total_active_balances, slashed_validator_balance, is_altair
    )

    # exiting_penalty
    while exiting_epoch <= EPOCHS_PER_SLASHING:
        balance, effective_balance = process_offline_penalty_altair_bellatrix(
            balance, effective_balance, total_active_balances
        )
        exiting_epoch += 1

    return balance, effective_balance


## Penalties Phase 0


def process_initial_penalty(balance: float, effective_balance: float) -> tuple:
    """
    Function to process the initial penalty
    """
    initial_penalty = effective_balance // MIN_SLASHING_PENALTY_QUOTIENT
    balance -= initial_penalty
    effective_balance = process_final_updates(balance, effective_balance)
    return balance, effective_balance


def process_offline_penalty(
    balance: float, effective_balance: float, total_active_balances: float
) -> tuple:
    """
    Function to process offline penalty
    """
    base_reward = (
        effective_balance
        * BASE_REWARD_FACTOR
        // integer_squareroot(total_active_balances)
    ) // BASE_REWARDS_PER_EPOCH
    offline_penalty = 3 * base_reward
    balance -= offline_penalty
    effective_balance = process_final_updates(balance, effective_balance)
    return balance, effective_balance


def process_special_penalty(
    balance: float,
    effective_balance: float,
    total_active_balances: float,
    slashed_validator_balance: float,
):
    """
    Function to process special penalty
    """
    special_penalty = (
        effective_balance
        * min(
            slashed_validator_balance * PROPORTIONAL_SLASHING_MULTIPLIER,
            total_active_balances,
        )
        // total_active_balances
    )
    balance -= special_penalty
    effective_balance = process_final_updates(balance, effective_balance)
    return balance, effective_balance


## Penalties Altair


def process_initial_penalty_altair_bellatrix(balance: float, effective_balance: float, is_altair: bool) -> tuple:
    """
    Function to process initial penalty altair or bellatrix
    """
    initial_penalty = effective_balance // MIN_SLASHING_PENALTY_QUOTIENT_ALTAIR if is_altair else effective_balance // MIN_SLASHING_PENALLTY_QUOTIENT_BELLATRIX
    balance -= initial_penalty
    effective_balance = process_final_updates(balance, effective_balance)
    return balance, effective_balance


def process_offline_penalty_altair_bellatrix(balance:float, effective_balance:float, total_active_balances:float):
    """
    Function to process offline penalty altair or bellatrix
    """
    base_reward = (
        effective_balance
        // EFFECTIVE_BALANCE_INCREMENT
        * (
            EFFECTIVE_BALANCE_INCREMENT
            * BASE_REWARD_FACTOR
            // integer_squareroot(total_active_balances)
        )
    )
    offline_penalty = (
        (TIMELY_SOURCE_WEIGHT + TIMELY_TARGET_WEIGHT + TIMELY_HEAD_WEIGHT)
        / WEIGHT_DENOMINATOR
        * base_reward
    )
    balance -= offline_penalty
    effective_balance = process_final_updates(balance, effective_balance)
    return balance, effective_balance


def process_special_penalty_altair_bellatrix(
    balance:float, effective_balance: float, total_active_balances: float, slashed_validator_balance: float, is_altair: bool
):
    """
    Function to process special penalty altair or bellatrix
    """

    special_penalty = (
        effective_balance
        * min(
            slashed_validator_balance * PROPORTIONAL_SLASHING_MULTIPLIER_ALTAIR,
            total_active_balances,
        )
        // total_active_balances
    ) if is_altair else (
        effective_balance
        * min(
            slashed_validator_balance * PROPORTIONAL_SLASHING_MULTIPLIER_BELLATRIX,
            total_active_balances,
        )
        // total_active_balances
    )
    balance -= special_penalty
    effective_balance = process_final_updates(balance, effective_balance)
    return balance, effective_balance


def process_sync_penalty_altair(balance: float, effective_balance, total_active_balances):
    """
    Function to process sync penalty altair
    """
    total_active_increments = total_active_balances // EFFECTIVE_BALANCE_INCREMENT
    total_base_rewards = (
        EFFECTIVE_BALANCE_INCREMENT
        * BASE_REWARD_FACTOR
        // integer_squareroot(total_active_balances)
        * total_active_increments
    )
    max_participant_rewards = (
        total_base_rewards * SYNC_REWARD_WEIGHT // WEIGHT_DENOMINATOR // SLOTS_PER_EPOCH
    )
    participant_reward = max_participant_rewards // SYNC_COMMITTEE_SIZE
    balance -= participant_reward
    effective_balance = process_final_updates(balance, effective_balance)
    return balance, effective_balance


## Final updates


def process_final_updates(balance: float, effective_balance: float) -> float:
    """
    Update effective balances with hysteresis
    """
    if (
        balance + DOWNWARD_THRESHOLD < effective_balance
        or effective_balance + UPWARD_THRESHOLD < balance
    ):
        effective_balance = min(
            balance - balance % EFFECTIVE_BALANCE_INCREMENT, MAX_EFFECTIVE_BALANCE
        )
    return effective_balance


## Helpers


def gwei_to_ether(amount: float|np.ndarray) -> float| np.ndarray:
    """
    Function to convert gwei to ether
    """
    return amount / 10**9


def integer_squareroot(n: float) -> float:
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x


def c(n: float, k: float) -> float:  
    """
    helper for large numbers binomial coefficient calculation
    """

    if 0 <= k <= n:
        nn = 1
        kk = 1
        for t in range(1, min(k, n - k) + 1):
            nn *= n
            kk *= t
            n -= 1
        return nn // kk
    else:
        return 0


def get_probability_outcomes(exam, validatorscount):
    outcome = []
    for offline_validator_sync_cnt in range(0, SYNC_COMMITTEE_SIZE + 1):
        outcome.append(
            c(int(exam), offline_validator_sync_cnt)
            * c(
                int(validatorscount - exam),
                SYNC_COMMITTEE_SIZE - offline_validator_sync_cnt,
            )
            / c(int(validatorscount), SYNC_COMMITTEE_SIZE)
        )
    df_outcome = pd.DataFrame(pd.Series(outcome), columns=["outcome"])
    df_outcome["cumul"] = df_outcome.outcome.cumsum()
    return df_outcome[df_outcome.cumul <= 0.99].tail(1).index[0]

