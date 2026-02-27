from __future__ import annotations
import skills
from skills import Skill
from effects import Effect


class Pokemon:
    name: str
    type: str

    def __init__(self, hp: int, attack: int, defense: int) -> None:
        # 初始化 Pokemon 的属性
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.skills = self.initialize_skills()
        self.alive = True
        self.statuses = []

    def initialize_skills(self):
        # 抽象方法，子类应实现具体技能初始化
        raise NotImplementedError

    def use_skill(self, skill: Skill, opponent: Pokemon):
        # 使用技能
        print(f"{self.name} uses {skill.name}")
        skill.execute(self, opponent)

    def heal_self(self, amount):
        # 为自身恢复生命值
        if not isinstance(amount, int):
            amount = int(amount)

        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        print(f"{self.name} heals {amount} HP! Current HP: {self.hp}/{self.max_hp}")

    def receive_damage(self, damage):
        # 计算伤害并减去防御力，更新 HP
        if not isinstance(damage, int):
            damage = int(damage)

        damage -= self.defense
        if damage <= 0:
            print(f"{self.name}'s defense absorbed the attack!")
            return

        self.hp -= damage
        print(
            f"{self.name} received {damage} damage! Remaining HP: {self.hp}/{self.max_hp}"
        )
        if self.hp <= 0:
            self.alive = False
            print(f"{self.name} has fainted!")

    def add_status_effect(self, effect: Effect):
        # 添加状态效果
        self.statuses.append(effect)

    def apply_status_effect(self):
        # 应用所有当前的状态效果，并移除持续时间结束的效果
        for status in self.statuses[:]:  # 使用切片防止列表在遍历时被修改
            status.apply(self)
            status.decrease_duration()
            if status.duration <= 0:
                print(f"{self.name}'s {status.name} effect has worn off.")
                self.statuses.remove(status)

    def type_effectiveness(self, opponent: Pokemon):
        # 计算属性克制的抽象方法，具体实现由子类提供
        raise NotImplementedError

    def begin(self):
        # 新回合开始时触发的方法
        pass

    def __str__(self) -> str:
        return f"{self.name} type: {self.type}"


# GlassPokemon 类
class GlassPokemon(Pokemon):
    type = "Glass"

    def type_effectiveness(self, opponent: Pokemon):
        # 针对敌方 Pokemon 的类型，调整效果倍率
        effectiveness = 1.0
        opponent_type = opponent.type

        if opponent_type == "Water":
            effectiveness = 2.0
        elif opponent_type == "Fire":
            effectiveness = 0.5
        return effectiveness

    def begin(self):
        # 每个回合开始时执行玻璃属性特性
        self.glass_attribute()

    def glass_attribute(self):
        # 玻璃属性特性：每回合恢复最大 HP 的 10%
        amount = self.max_hp * 0.1
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        print(
            f"{self.name} heals {amount} HP at the start of the turn! Current HP: {self.hp}/{self.max_hp}"
        )


# Bulbasaur 类，继承自 GlassPokemon
class Bulbasaur(GlassPokemon):
    name = "Bulbasaur"

    def __init__(self, hp=100, attack=50, defense=10) -> None:
        # 初始化 Bulbasaur 的属性
        super().__init__(hp, attack, defense)

    def initialize_skills(self):
        # 初始化技能，具体技能是 SeedBomb 和 ParasiticSeeds
        return [skills.SeedBomb(damage=50), skills.ParasiticSeeds(amount=10)]

# ElectricPokemon 类
class ElectricPokemon(Pokemon):
    type = "Electric"

    def type_effectiveness(self, opponent: Pokemon):
        # 针对敌方 Pokemon 的类型，调整效果倍率
        effectiveness = 1.0
        opponent_type = opponent.type

        if opponent_type == "Water":
            effectiveness = 2.0
        elif opponent_type == "Glass":
            effectiveness = 0.5
        return effectiveness

    def begin(self):
        # 每个回合开始时执行玻璃属性特性
        self.elec_attribute()
 

    def elec_attribute(self):
        #######################################################################
        amount = self.max_hp * 0.1
        self.hp += amount


# PikaChu 类，继承自 ElectricPokemon
class PikaChu(ElectricPokemon):
    name = "PikaChu"

    def __init__(self, hp=80, attack=35, defense=5) -> None:
        # 初始化 Bulbasaur 的属性
        super().__init__(hp, attack, defense)

    def initialize_skills(self):
        # 初始化技能，具体技能是 SeedBomb 和 ParasiticSeeds
        return [skills.QuickAttack(1.0*attack),skills.Thunderbolt(1.4*self.attack)]
    

# WaterPokemon 类
class WaterPokemon(Pokemon):
    type = "Water"

    def type_effectiveness(self, opponent: Pokemon):
        # 针对敌方 Pokemon 的类型，调整效果倍率
        effectiveness = 1.0
        opponent_type = opponent.type

        if opponent_type == "Fire":
            effectiveness = 2.0
        elif opponent_type == "Electric":
            effectiveness = 0.5
        return effectiveness

    def begin(self):
        self.water_attribute()

    def water_attribute(self,opponent:"Pokemon"):
        if random.randint(1, 100) <= 50:
           opponent.attack *= 0.7
           print(f"30% off !")
        else:
            print(f"eat all.")


# Parasitic Seeds 类，继承自 WaterPokemon
class ParasiticSeeds(WaterPokemon):
    name = "Parasitic Seeds"

    def __init__(self, hp=80, attack=25, defense=20) -> None:
        super().__init__(hp, attack, defense)

    def initialize_skills(self):
        # 初始化技能，具体技能是 SeedBomb 和 ParasiticSeeds
        return [skills.AquaJet(1.4*self.attack),skills.Shield(0.5)]
    
    
# FirePokemon 类
class FirePokemon(Pokemon):
    type = "Water"

    def type_effectiveness(self, opponent: Pokemon):
        # 针对敌方 Pokemon 的类型，调整效果倍率
        effectiveness = 1.0
        opponent_type = opponent.type

        if opponent_type == "Glass":
            effectiveness = 2.0
        elif opponent_type == "Water":
            effectiveness = 0.5
        return effectiveness

    def begin(self):
        self.fire_attribute()

    def fire_attribute(self):
        self.attack *= 1.1
        
# Charmander 类，继承自 FirePokemon
class Charmander(FirePokemon):
    name = "Charmander"

    def __init__(self, hp=80, attack=35, defense=15) -> None:
        super().__init__(hp, attack, defense)

    def initialize_skills(self):
        # 初始化技能，具体技能是 SeedBomb 和 ParasiticSeeds
        return [skills.Ember(self.attack),skills.FlameCharge(3*self.attack)]
    
# MewtwoPokemon 类
class MewtwoPokemon(Pokemon):
    type = "Water"

    def type_effectiveness(self, opponent: Pokemon):
        # 针对敌方 Pokemon 的类型，调整效果倍率
        effectiveness = 1.0
        opponent_type = opponent.type

        if opponent_type == "":
            effectiveness = 2.0
        elif opponent_type == "":
            effectiveness = 0.5
        return effectiveness

    def begin(self):
        self.fire_attribute()

    def mew_attribute(self):
########################################################
        self.attack *= 1
        


# Latios 类，继承自 MewtwoPokemon
class Latios(MewtwoPokemon):
    name = "Charmander"

    def __init__(self, hp=80, attack=130, defense=110) -> None:
        super().__init__(hp, attack, defense)

    def initialize_skills(self):
        # 初始化技能，具体技能是 SeedBomb 和 ParasiticSeeds
        return [skills.Psychic(self.attack),skills.CalmMind()]
    