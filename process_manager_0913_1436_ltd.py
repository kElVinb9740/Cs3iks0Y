# 代码生成时间: 2025-09-13 14:36:13
import asyncio
from sanic import Sanic, response
from sanic.exceptions import ServerError
from subprocess import Popen, PIPE
import psutil
import signal
import sys

def handle_signal(signum, frame):
    """
    Handle the signal to gracefully shutdown the process manager.
    """
    print(f'Signal {signum} received, shutting down...')
    sys.exit(0)
    

# Register signal handlers
signal.signal(signal.SIGTERM, handle_signal)
signal.signal(signal.SIGINT, handle_signal)

app = Sanic("ProcessManager")

@app.route('/run/<command>', methods=['GET'])
async def run_process(request, command):
    """
    Run a process command and return the output.
    """
    try:
        # Split the command into list of arguments
        args = command.split(' ')
        # Run the process
        process = Popen(args, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        # Return the output of the process
        return response.json({'stdout': stdout.decode(), 'stderr': stderr.decode()})
    except Exception as e:
        # Handle any errors that occur during process execution
        raise ServerError("Failed to run process", e)

@app.route('/list', methods=['GET'])
async def list_processes(request):
    """
    List all running processes.
    """
    try:
        # Get all running processes
        processes = psutil.process_iter(['pid', 'name', 'status'])
        # Convert the process information into a list
        process_list = [{'pid': p.info['pid'], 'name': p.info['name'], 'status': p.info['status']} for p in processes]
        # Return the list of processes
        return response.json(process_list)
    except Exception as e:
        # Handle any errors that occur while listing processes
        raise ServerError("Failed to list processes", e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, workers=1)
