import asyncio
from house_valve_client import HouseValveClient

async def main():
    # 待处理的采集箱编号列表
    collector_serial_numbers = [
        25012508,25012704,25012197,25012210,25012342,25013098,25013105,25013145,25014238,25014953,25015035,25015056,25015069,25013134,25013139,25012172,25012174,25012186,25012199,25012215,25012341,25012344,25013077,25013102,25013123,25014994,25015019,25012192,25012195,25012222,25012421,25012665,25012672,25012778,25012792,25013107,25013125,25013186,25013245,25012212,25012315,25012906,25012940,25012962,25012966,25012968,25012911,25012243,25012347,25012890,25013089,25013142,25013177,24006286,24006515,24000701,24000742,24000783,24001007,24001028,24001032,24001034,24001040,24001095,24001117,24006731,13180096,131800070,25013074,25013127,25012691,25012693,25012822,25013118,25012710,25013183,25012701,25012706,25012712,25013200,25013234,25015008,25012082,25012144,25012266,25012309,25013190,25013246,25014971,25012592,25012594,25012673,25012761,25012831,24480196,25013013,25003401,24006301,24006306,24006341,24006483,24006598,24006608,24006670,24006923,25012493,25012506,25012507,25012634,25012796,25012797,25013174,25012647
    ]
    
    try:
        # 初始化客户端
        async with HouseValveClient(
            base_url="http://112.53.73.250:2288",
            token="a704c946-b32e-49eb-85d8-f0a576695d78"
        ) as client:
            print("=== 开始更新采集箱档案 ===")
            print(f"共 {len(collector_serial_numbers)} 个采集箱需要更新")
            print(f"采集箱编号列表: {collector_serial_numbers}")
            
            # 调用update_control_by_serial_no方法更新档案
            result = await client.update_control_by_serial_no(collector_serial_numbers)
            
            # 打印结果
            print(f"\n更新结果: {'成功' if result['success'] else '失败'}")
            print(f"消息: {result['message']}")
            
            if result['update_result']:
                print(f"\nAPI返回: {result['update_result']}")
            
            # 打印设备详情
            print(f"\n设备详情 ({len(result['device_info'])} 个):")
            found_count = 0
            not_found_count = 0
            
            for device in result['device_info']:
                status = "成功" if device['found'] else "失败"
                if device['found']:
                    found_count += 1
                else:
                    not_found_count += 1
                print(f"  - serial_no: {device['serial_no']}, guid: {device['guid']}, 状态: {status}")
            
            print(f"\n统计信息:")
            print(f"  总数量: {len(result['device_info'])}")
            print(f"  成功获取GUID: {found_count}")
            print(f"  未找到GUID: {not_found_count}")
    except Exception as e:
        print("\n=== 错误信息 ===")
        print(f"发生异常: {str(e)}")
        print("\n建议检查:")
        print("1. 请确保提供了有效的token")
        print("2. 请检查网络连接是否正常")
        print("3. 请确认API地址是否正确")
        print("4. 请联系系统管理员获取有效的认证信息")

if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())
