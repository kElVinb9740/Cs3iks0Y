# 代码生成时间: 2025-09-20 05:35:10
import asyncio
import psutil
from sanic import Sanic, response

# 创建一个Sanic的app实例
app = Sanic("ProcessManager")

# 定义一个函数，用于获取所有进程信息
async def get_all_processes():
    # 通过psutil获取所有进程信息
    processes = []
    for proc in psutil.process_iter(["pid", "name", "status"], ad_value=None):
        try:
            process_info = {
                "pid": proc.info["pid"],
                "name": proc.info["name"],
                "status": proc.info["status"]
            }
            processes.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # 忽略无法访问的进程
            continue
    return processes

# 定义一个函数，用于结束指定进程
async def terminate_process(pid):
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        proc.wait()
        return {"status": "Process terminated"}
    except psutil.NoSuchProcess:
        return {"status": "Process not found"}
    except psutil.AccessDenied:
        return {"status": "Access denied"}
    except psutil.TimeoutExpired:
        return {"status": "Timeout expired"}

# 定义一个Sanic路由，用于获取所有进程信息
@app.route("/processes", methods=["GET"])
async def get_processes(request):
    processes = await get_all_processes()
    return response.json(processes)

# 定义一个Sanic路由，用于结束指定进程
@app.route("/process/<pid:int>", methods=["DELETE"])
async def terminate_process_handler(request, pid):
    result = await terminate_process(pid)
    return response.json(result)

# 定义一个主函数，用于启动Sanic应用
def main():
    app.run(host="0.0.0.0", port=8000)

# 直接调用main函数启动应用
if __name__ == "__main__":
    main()