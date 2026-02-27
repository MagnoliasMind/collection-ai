import sys
from story_data import DIALOGUES, GIFT_EFFECTS
class Character:
    def __init__(self, name, role, affinity=0):
        self.name = name
        self.role = role
        self.affinity = affinity
        self.dialogue_count = 0
    def talk(self,dialogues):
        
        character_dialogues = DIALOGUES.get(self.name, [])
       
        #if not hasattr(self, "dialogue_count"):
             #self.dialogue_count = 0
    
        current_idx = self.dialogue_count % len(character_dialogues)
        self.dialogue_count += 1  
    
    
        current_dialogue = character_dialogues[current_idx]
        print(f"{self.name}:{current_dialogue['text']}") 
    
        print(f"A. {current_dialogue['optionA']}")
        print(f"B. {current_dialogue['optionB']}")
        choice = input("请选择回复：")
    
    
        if choice == "A":
            change_value = current_dialogue["key1"]  # 读取key1的值
            self.change_affinity(change_value)
            
            print(f"对方对你的好感度提升了{change_value}！")
        elif choice == "B":
            change_value = current_dialogue["key2"]  # 读取key1的值
            self.change_affinity(change_value)
            
            print(f"对方对你的好感度提升了{change_value}！")
        else:
            print(f"你的回复有点奇怪，对方没太在意...")
            
        
        # TODO: 补充具体对话，对话内容可以从剧本里面截取 根据主人公的不同，使用不同的对话（你也可以根据好感度的不同/对话次数的不同 改变对话和选项）
        

    def give_gift(self, gift,gift_effects):
       gift_data = GIFT_EFFECTS.get(gift, {})
       print(f"你送给 {self.name} 一份 {gift}。")
   
       value = int(gift_data.get(self.name, gift_data.get("default", 0)))
    
       self.change_affinity(value)

        # TODO: 完成礼物好感度逻辑（送出不同礼物加不同的好感度） 并调用change_affinity（）函数 传入此次好感度变化的数值value
       pass

    def change_affinity(self,value,other=0):
        self.affinity += value
        print(f"{self.name} 的好感度变化 {value} -> 当前好感度：{self.affinity}")

    def check_ending(self,other=0):
        if self.affinity >= 100:
            print(f"恭喜！你和 {self.name} 的故事进入了结局线！")
            return True
        return False
