import logging
import os
import subprocess
import sys

from helpers.consistency_result import ProverResult

default_vampire_modes = ['casc_sat','casc','portfolio']


def decide_whether_theory_is_consistent(theory_file_name: str, keep_temp_files=True, vampire_modes=default_vampire_modes) -> ProverResult:
    vampire_modes = vampire_modes.copy()
    vampire_input_file_name = theory_file_name + '.in'
    vampire_output_file_name = theory_file_name + '.out'
    cmd_to_run_vampire = 'resources/vampire --mode ' + vampire_modes[0] + '  ' + vampire_input_file_name + ' > ' + vampire_output_file_name
    vampire_process = subprocess.Popen(cmd_to_run_vampire, shell=True)
    vampire_process.wait()
    vampire_has_decided = vampire_process.returncode == 0
    vampire_process.kill()
    if vampire_has_decided:
        theory_with_i_identity_criterionconsistency_check_file = open(vampire_output_file_name)
        theory_with_i_identity_criterionconsistency_check = theory_with_i_identity_criterionconsistency_check_file.read()
        theory_with_i_identity_criterionconsistency_check_file.close()
        if not keep_temp_files:
            os.remove(vampire_input_file_name)
            os.remove(vampire_output_file_name)
        
        if 'SZS status Theorem' in theory_with_i_identity_criterionconsistency_check:
            return ProverResult.THEOREM
        if 'SZS status Unsatisfiable' in theory_with_i_identity_criterionconsistency_check:
            return ProverResult.INCONSISTENT
        if 'SZS status Satisfiable' in theory_with_i_identity_criterionconsistency_check:
            return ProverResult.CONSISTENT
        if 'SZS status CounterSatisfiable' in theory_with_i_identity_criterionconsistency_check:
            return ProverResult.COUNTERSATISFIABLE
        logging.error(msg='Vampire hit a bump' + str(vampire_process))
        sys.exit(-1)
    else:
        vampire_modes.pop(0)
        if len(vampire_modes) > 0:
            logging.info(msg='Trying mode ' + vampire_modes[0])
            return \
                decide_whether_theory_is_consistent(
                    theory_file_name=theory_file_name,
                    keep_temp_files=keep_temp_files,
                    vampire_modes=vampire_modes)
        return ProverResult.UNDECIDED
