import random
from typing import TYPE_CHECKING
import effects

if TYPE_CHECKING:
    from pokemon import Pokemon


class Skill:
    name: str

    def __init__(self) -> None:
        pass

    def execute(self, user: "Pokemon", opponent: "Pokemon"):
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{self.name}"


class SeedBomb(Skill):
    name = "Seed Bomb"

    def __init__(self, damage: int, activation_chance: int = 15) -> None:
        super().__init__()
        self.damage = damage
        self.activation_chance = activation_chance  # 确保激活几率被正确初始化

    def execute(self, user: "Pokemon", opponent: "Pokemon") -> None:
        # 造成伤害
        opponent.receive_damage(self.damage)
        print(
            f"{user.name} used {self.name}, dealing {self.damage} damage to {opponent.name}"
        )

        # 判断是否触发状态效果
        if random.randint(1, 100) <= self.activation_chance:
            opponent.add_status_effect(effects.PoisonEffect())
            print(f"{opponent.name} is poisoned by {self.name}!")
        else:
            print(f"{self.name} did not poison {opponent.name} this time.")


class ParasiticSeeds(Skill):
    name = "Parasitic Seeds"

    def __init__(self, amount: int) -> None:
        super().__init__()
        self.amount = amount

    def execute(self, user: "Pokemon", opponent: "Pokemon") -> None:
        # 给使用者添加治疗效果
        user.add_status_effect(effects.HealEffect(self.amount))
        print(f"{user.name} heals {self.amount} HP with {self.name}")

        # 给对手添加中毒效果
        opponent.add_status_effect(effects.PoisonEffect())
        print(f"{opponent.name} is poisoned by {self.name}!")

class Thunderbolt(Skill):
    name = "Thunderbolt"
    
    def __init__(self, damage: int, activation_chance: int = 10)->None:
        super().__init__()
        self.amount = self.amount
        
    def excute(self,user: "Pokemon",opponent:"Pokemon")->None:
        # 造成伤害
        opponent.receive_damage(self.damage)
        print(
            f"{user.name} used {self.name}, dealing {self.damage} damage to {opponent.name}"
        )
     # 判断是否触发状态效果 #############################################################
        if random.randint(1, 100) <= self.activation_chance:
            opponent.add_status_effect(effects.Paralysis())
            print(f"{opponent.name} is slow down !")
        else:
            print(f"{self.name} did not affected {opponent.name} this time.")
    
    
class QuickAttack(Skill):
    name = "Quick Attack"
    
    def __init__(self, damage: int, activation_chance: int = 10)->None:
        super().__init__()
        self.amount = self.amount
        
    def excute(self,user: "Pokemon",opponent:"Pokemon")->None:
        # 造成伤害
        opponent.receive_damage(self.damage)
        print(
            f"{user.name} used {self.name}, dealing {self.damage} damage to {opponent.name}"
        )
        
    # 判断是否触发状态效果
        if random.randint(1, 100) <= self.activation_chance:
            opponent.receive_damage(self.damage)
            print(f"{opponent.name} is double attacked by {self.name}!")
        else:
            print(f"{self.name} did not attacked  {opponent.name} twice.")
            
class AquaJet(Skill):
    name = "Aqua Jet"
    
    def __int__(self,damage:int)->None:
        super().__init__()
        self.amount = self.amount
        
    def excute(self,user: "Pokemon",opponent:"Pokemon")->None:
        # 造成伤害
        opponent.receive_damage(self.damage)
        print(
            f"{user.name} used {self.name}, dealing {self.damage} damage to {opponent.name}"
        )
        
class Shield(Skill):
    name = "Shield"
    
    def __init__(self, amount: float) -> None:
        super().__init__()
        self.amount = amount
        
    def execute(self, user:"Pokemon",opponent:"Pokemon"):
        user.receive_damage(opponent.attack*amount)
        
class Ember(Skill):
    name = "Ember"
    
    def __init__(self, damage: int, activation_chance: int = 10)->None:
        super().__init__()
        self.amount = self.amount
        
    def excute(self,user: "Pokemon",opponent:"Pokemon")->None:
        # 造成伤害
        opponent.receive_damage(self.damage)
        print(
            f"{user.name} used {self.name}, dealing {self.damage} damage to {opponent.name}"
        )

        if random.randint(1, 100) <= self.activation_chance:
            opponent.add_status_effect(effects.Burning())
            print(f"{opponent.name} is burning !")
        else:
            print(f"{self.name} did not ignite {opponent.name} this time.")
            
class FlameCharge(Skill):
    name = "Flame Charge"
    
    def __init__(self, damage: int, activation_chance: int = 80)->None:
        super().__init__()
        self.amount = self.amount
        
    def excute(self,user: "Pokemon",opponent:"Pokemon")->None:
        # 造成伤害
        opponent.receive_damage(self.damage)
        print(
            f"{user.name} used {self.name}, dealing {self.damage} damage to {opponent.name}"
        )
        
        if random.randint(1, 100) <= self.activation_chance:
            opponent.add_status_effect(effects.Burning())
            print(f"{opponent.name} is burning !")
        else:
            print(f"{self.name} did not ignite {opponent.name} this time.")
            
class Psychic(Skill):
    name = "Psychic"
    
    def __init__(self, damage: int, activation_chance: int = 10)->None:
        super().__init__()
        self.amount = self.amount
        
    def excute(self,user: "Pokemon",opponent:"Pokemon")->None:
        # 造成伤害
        opponent.receive_damage(self.damage)
        print(
            f"{user.name} used {self.name}, dealing {self.damage} damage to {opponent.name}"
        )
        
class CalmMind(Skill):
    name = "Calm Mind"
    
    def __init__(self):
        super().__init__()
        
class Psychic(Skill):
    name = "Psychic"
    
    def __init__(self, damage: int, activation_chance: int = 10)->None:
        super().__init__()
        self.amount = self.amount
        
    def excute(self,user: "Pokemon",opponent:"Pokemon")->None:
        # 造成伤害
        opponent.receive_damage(self.damage)
        print(
            f"{user.name} used {self.name}, dealing {self.damage} damage to {opponent.name}"
        )
        
        if random.randint(1, 100) <= activation_chance:
            opponent.add_status_effect(effects.Defend(2,0.9))
            print(f"{opponent.name}'s defense is decrese to 90% !")
        else:
            print(f"{self.name} did not affect {opponent.name} this time.")
            
class CalmMind(Skill):
    name = "Calm Mind"
    
    def __init__(self,activation_chance: int = 20)->None:
        super().__init__()
        
    def excute(self,user: "Pokemon")->None:
        # 造成伤害
        if random.randint(1, 100) <= activation_chance:
            self.attack *= 1.5
            self.defence *=1.5
            print(f"{self.name}'s defense and attack is increse to 150% !")
        else:
            print(f"{self.name} did not change this time.")
            