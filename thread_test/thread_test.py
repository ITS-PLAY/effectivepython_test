import subprocess
# # Enable these lines to make this example work on Windows
# import os
# os.environ['COMSPEC'] = 'powershell'
#
# result = subprocess.run(
#     ['echo', 'Hello from the child!'],
#     capture_output=True,
#     # Enable this line to make this example work on Windows
#     shell=True,
#     encoding='utf-8')
#
# result.check_returncode()  # No exception means it exited cleanly
# print(result.stdout)

"""example 2"""
# proc = subprocess.Popen(['sleep', '1'], shell=True)
# while proc.poll() is None:
#     print('Working...')
#     import time
#     time.sleep(0.3)
#
# print('Exit status', proc.poll())

"""example 3"""
# import time
# start = time.time()
# sleep_procs =[]
# for _ in range(10):
#     proc = subprocess.Popen(['sleep', '1'], shell=True)
#     sleep_procs.append(proc)
#
# for proc in sleep_procs:
#     proc.communicate()
#
# end = time.time()
# delta = end - start
# print('finished in {} seconds'.format(delta))

"""example 4"""
# import os
# def run_encrypt(data):
#     env = os.environ.copy()
#
#     env['password'] = 'zf7ShyBhZOraQDde/fizpm/m/8f9x+m1'
#     proc = subprocess.Popen(['openssl', 'enc', '-des3', '-pass', 'env:password'],
#                             env=env,
#                             stdin=subprocess.PIPE,
#                             stdout=subprocess.PIPE)
#     proc.stdin.write(data)
#     proc.stdin.flush()
#     return proc
#
# procs = []
# for _ in range(3):
#     data = os.urandom(10)
#     proc = run_encrypt(data)
#     procs.append(proc)
#
# for proc in procs:
#     out, _ = proc.communicate()
#     print(out[-10:])


"""example 5"""
import os
def run_encrypt(data):
    env = os.environ.copy()

    env['password'] = 'zf7ShyBhZOraQDde/fizpm/m/8f9x+m1'
    proc = subprocess.Popen(['openssl', 'enc', '-des3', '-pass', 'env:password'],
                            env=env,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    proc.stdin.write(data)
    proc.stdin.flush()
    return proc

def run_hash(input_stdin):
    return subprocess.Popen(['openssl', 'dgst', '-whirlpool', '-binary'],
                            stdin=input_stdin,
                            stdout=subprocess.PIPE)

# encrypt_procs = []
# hash_procs =[]
# for _ in range(3):
#     data = os.urandom(100)
#     encrypt_proc = run_encrypt(data)
#     encrypt_procs.append(encrypt_proc)
#
#     hash_proc = run_hash(encrypt_proc.stdout)
#     hash_procs.append(hash_proc)
#
#     encrypt_proc.stdout.close()
#     encrypt_proc.stdout = None
#
# for proc in encrypt_procs:
#     proc.communicate()
#     assert proc.returncode == 0
#
# for proc in hash_procs:
#     out, _ = proc.communicate()
#     print(out[-10:])
#     assert proc.returncode == 0

"""example 6"""
proc = subprocess.Popen(['sleep', '10'], shell=True)
try:
    proc.communicate(timeout=0.1)
except subprocess.TimeoutExpired:
    proc.terminate()
    proc.wait()

print('exit status', proc.poll())
