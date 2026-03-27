import json
import random
import datetime
from typing import Dict, List, Tuple

class CampusHealthAssistant:
    """校园健康助手核心类"""
    
    def __init__(self):
        """初始化健康知识库和对话历史"""
        self.health_knowledge = {
            "睡眠": [
                "建议保持规律的作息时间，每天固定时间睡觉和起床",
                "睡前1小时避免使用电子设备，可以尝试阅读或冥想",
                "大学生每天应保证7-9小时的睡眠时间",
                "午睡时间不宜超过30分钟，以免影响夜间睡眠"
            ],
            "压力": [
                "进行适量运动，如每天30分钟的快走或慢跑",
                "尝试深呼吸练习：吸气4秒，屏气7秒，呼气8秒",
                "将大任务分解为小目标，逐步完成",
                "与朋友、家人或心理咨询师倾诉你的感受"
            ],
            "饮食": [
                "每天摄入5种不同颜色的蔬菜水果",
                "保证充足的水分摄入，每天至少1.5升水",
                "避免过度依赖咖啡因和含糖饮料",
                "早餐要吃好，提供一天所需的能量"
            ],
            "运动": [
                "每周至少进行150分钟中等强度有氧运动",
                "结合有氧运动和力量训练，效果更佳",
                "利用校园设施，如操场、健身房进行锻炼",
                "运动前热身5-10分钟，运动后拉伸放松"
            ]
        }
        self.conversation_history = []
        self.user_profile = {}
        
    def analyze_query(self, user_input: str) -> Tuple[str, float]:
        """分析用户问题，返回问题类型和置信度"""
        input_lower = user_input.lower()
        categories = {
            "睡眠": ["睡", "失眠", "熬夜", "困", "作息"],
            "压力": ["压力", "焦虑", "紧张", "累", "心烦"],
            "饮食": ["吃", "饮食", "营养", "减肥", "健康食品"],
            "运动": ["运动", "锻炼", "健身", "跑步", "体育"]
        }
        
        best_match = "综合健康"
        max_score = 0.0
        
        for category, keywords in categories.items():
            score = sum(1 for keyword in keywords if keyword in input_lower)
            if score > max_score:
                max_score = score
                best_match = category
                
        confidence = min(max_score / 5, 1.0)
        return best_match, confidence
    
    def generate_response(self, user_input: str, user_id: str = "default") -> Dict:
        """生成AI回答，模拟大模型响应"""
        # 记录对话历史
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conversation_history.append({
            "user_id": user_id,
            "timestamp": timestamp,
            "query": user_input,
            "type": "user"
        })
        
        # 分析问题类型
        category, confidence = self.analyze_query(user_input)
        
        # 根据问题类型生成回答
        if category in self.health_knowledge and confidence > 0.3:
            answers = self.health_knowledge[category]
            response = random.choice(answers)
            source = "专业健康知识库"
        else:
            response = "我主要专注于睡眠、压力、饮食和运动方面的健康咨询。您可以具体描述一下您的情况吗？"
            source = "通用回复模板"
            category = "综合健康"
        
        # 添加个性化建议
        if "经常" in user_input or "总是" in user_input:
            response += " 如果问题持续存在，建议咨询校医院的专业医生。"
        
        # 构建响应数据
        ai_response = {
            "response": response,
            "category": category,
            "confidence": round(confidence, 2),
            "source": source,
            "timestamp": timestamp,
            "response_id": f"resp_{len(self.conversation_history)}"
        }
        
        # 记录AI响应
        self.conversation_history.append({
            "user_id": user_id,
            "timestamp": timestamp,
            "response": ai_response,
            "type": "ai"
        })
        
        return ai_response
    
    def get_conversation_stats(self, user_id: str = "default") -> Dict:
        """获取对话统计信息，用于优化分析"""
        user_chats = [c for c in self.conversation_history if c["user_id"] == user_id]
        ai_responses = [c for c in user_chats if c["type"] == "ai"]
        
        categories = []
        for resp in ai_responses:
            if "response" in resp:
                categories.append(resp["response"].get("category", "未知"))
        
        return {
            "total_conversations": len(user_chats) // 2,
            "ai_responses_count": len(ai_responses),
            "common_categories": max(set(categories), key=categories.count) if categories else "无",
            "last_active": user_chats[-1]["timestamp"] if user_chats else "从未使用"
        }
    
    def optimize_based_on_feedback(self, response_id: str, is_helpful: bool):
        """模拟基于反馈的优化（简化版）"""
        print(f"收到反馈：响应 {response_id} {'有帮助' if is_helpful else '无帮助'}")
        if not is_helpful:
            print("已记录该反馈，将用于优化后续回答准确性")

def main():
    """主函数：模拟校园健康助手运行"""
    print("=" * 50)
    print("校园健康助手 AI 问答系统")
    print("=" * 50)
    
    # 初始化助手
    assistant = CampusHealthAssistant()
    
    # 模拟用户对话
    test_queries = [
        "最近总是失眠怎么办？",
        "学习压力大，感觉很焦虑",
        "如何保持健康的饮食习惯？",
        "经常头疼是什么原因"
    ]
    
    print("\n模拟用户咨询场景：")
    print("-" * 30)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n用户{i}: {query}")
        response = assistant.generate_response(query, f"user_{i}")
        
        print(f"AI助手: {response['response']}")
        print(f"   [分类: {response['category']}, 置信度: {response['confidence']}]")
    
    # 显示统计信息
    print("\n" + "=" * 50)
    print("对话统计分析：")
    print("-" * 30)
    
    for i in range(1, len(test_queries) + 1):
        stats = assistant.get_conversation_stats(f"user_{i}")
        print(f"用户{i}: {stats['total_conversations']}次咨询，"
              f"主要关注: {stats['common_categories']}")
    
    # 模拟优化反馈
    print("\n" + "=" * 50)
    print("优化模拟：")
    print("-" * 30)
    assistant.optimize_based_on_feedback("resp_2", True)
    assistant.optimize_based_on_feedback("resp_4", False)
    
    print("\n系统运行完成！")
    print("注：实际项目中会连接真实大模型API")

if __name__ == "__main__":
    main()