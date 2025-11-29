import requests

class JDCookie:
    def __init__(self, cookie):
        self.cookie = cookie
        self.api_url = "http://xxxxx:5700/open" ##你的内网路径
        self.client_id = 'xxxxx'
        self.client_secret = 'xxxxxx'
    def get_token(self):
        """获取青龙面板的token大致一个月过期"""
        client={'client_id':self.client_id,'client_secret':self.client_secret}
        get_token=requests.get(self.api_url+"/auth/token",params=client)
        get_token_json=get_token.json()
        token=get_token_json['data']['token']
        return token
    def get_headers(self):
        """拼凑请求头将token加入请求头"""
        token=self.get_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "accept": "application/json"
        }
        return headers
    def get_envs(self):
        """打印所有环境变量,有一些id和看到的不一样，需要注意"""
        headers=self.get_headers()
        envs=requests.get(self.api_url+"/envs", headers=headers)
        print(envs.text)
    def update_envs(self):
        """更新JD_COOKIE环境变量"""
        headers=self.get_headers()
        data = {
            "value": f"{self.cookie}",
            "name": "JD_COOKIE",
            "remarks": "京东cookie",
            "id": "1"
        }
        env_update=requests.put(self.api_url+"/envs", headers=headers, json=data)
    def run_task(self):
        """执行京东相关任务"""
        headers=self.get_headers()
        cron_mission=requests.get(self.api_url+"/crons", headers=headers)
        cron_mission_json=cron_mission.json()
        task_id=cron_mission_json['data']
        JD_Task_Id=[ listdata['id'] for listdata in cron_mission_json['data'].get('data')
            if listdata['sub_id']==2 # 京东相关任务的sub_id为2
        ]
        JD_task_run=requests.put(self.api_url+f"/crons/run", headers=headers,data=f'{JD_Task_Id}')
        if JD_task_run.status_code==200:
            print("任务执行成功")
        else:
            print("任务执行失败")
    def run(self):
        self.update_envs()
        self.run_task()

if __name__ == "__main__":
    cookie = "pt_key=xxxxxxxxxxxx;pt_pin=xxxxxxxxxxx;"
    jd_cookie_manager = JDCookie(cookie)
    jd_cookie_manager.run()
