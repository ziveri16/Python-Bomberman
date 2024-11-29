from actor import *
import random
import g2d

MAP_WIDTH = 928
MAP_HEIGHT = 416
ALIGNMENT_TOLERANCE = 16

#FUNZIONI GENERICHE
def check_overlap(a1: Actor, a2: Actor) -> bool:
    x1, y1, w1, h1 = a1.pos() + a1.size()
    x2, y2, w2, h2 = a2.pos() + a2.size()
    return (y2 < y1 + h1 and y1 < y2 + h2 and
            x2 < x1 + w1 and x1 < x2 + w2)

# cla

class Ddoor():
    def __init__(self, pos: tuple, size=(32, 32)):
        self._x, self._y = pos
        self._w, self._h = size
        self._accessible = False
        self._hidden_porta = True

    def pos(self) -> Point:
        return self._x, self._y
    
    def size(self) -> Point:
        return self._w, self._h
    def sprite(self) -> str:
        return "png/dDoor.png"
    def move(self, arena : Arena):
        pass

class Giocatore():
    def __init__(self):
        self._bomberman_alive = True
        self._bombergirl_alive = True
        self._life = 3
        self._time = 160
        self._points = 100
        self._conta_tempo = 0
        self._level = 1
        self._win = False


    def check_timer(self):
        self._conta_tempo +=1
        if self._conta_tempo % 30 == 0:
            self._time -= 1

    def check_for_win(self, arena : Arena) -> int:
        enemies_count = 0
        for actor in arena.actors():
            if isinstance(actor, Ballom) or isinstance(actor, Iceman):
                enemies_count += 1

        return enemies_count

    def get_points(self):
        return(round((self._points / 100) * 100))

            
class Destructible_Block_Death(Actor):
    def __init__(self, pos: tuple):
        self._x, self._y = pos
        self._w, self._h = 32, 32
        self._death_sprites = ["png/destroyed1.png", "png/destroyed2.png", "png/destroyed3.png", "png/destroyed4.png", "png/destroyed5.png", "png/destroyed6.png"]
        self._death_lenght = 50
        self._animation_index_death = 0
        self._animation_counter_death = 0

    def pos(self) -> Point:
        return self._x, self._y
    
    def size(self) -> Point:
        return self._w, self._h
    
    def sprite(self) -> str:
        return self._death_sprites[self._animation_index_death]
    
    def move(self, arena : Arena):
        if self._death_lenght <= 0:
            arena.kill(self)
        else:
            self._animation_counter_death = (self._animation_counter_death + 1) % 10 #rallentiamo il cambio di frame
            if self._animation_counter_death == 0:
                self._animation_index_death = (self._animation_index_death + 1) % len(self._death_sprites)
            self._death_lenght -= 1

class Bomberman_Death(Actor):
    def __init__(self, pos: tuple):
        self._x, self._y = pos
        self._w, self._h = 32, 32
        self._death_sprites = ["png/bomberman_death1.png", "png/bomberman_death2.png", "png/bomberman_death3.png", "png/bomberman_death4.png", "png/bomberman_death5.png", "png/bomberman_death6.png", "png/bomberman_death7.png"]
        self._death_lenght = 60
        self._animation_index_death = 0
        self._animation_counter_death = 0

    def pos(self) -> Point:
        return self._x, self._y
    
    def size(self) -> Point:
        return self._w, self._h
    
    def sprite(self) -> str:
        return self._death_sprites[self._animation_index_death]
    
    def move(self, arena : Arena):
        if self._death_lenght <= 0:
            arena.kill(self)
        else:
            self._animation_counter_death = (self._animation_counter_death + 1) % 10 #rallentiamo il cambio di frame
            if self._animation_counter_death == 0:
                self._animation_index_death = (self._animation_index_death + 1) % len(self._death_sprites)
            self._death_lenght -= 1
         
class Bombergirl_Death(Actor):
    def __init__(self, pos: tuple):
        self._x, self._y = pos
        self._w, self._h = 32, 32
        self._death_sprites = ["png/bombergirl_death1.png", "png/bombergirl_death2.png", "png/bombergirl_death3.png", "png/bombergirl_death4.png", "png/bombergirl_death5.png", "png/bombergirl_death6.png", "png/bombergirl_death7.png"]
        self._death_lenght = 60
        self._animation_index_death = 0
        self._animation_counter_death = 0

    def pos(self) -> Point:
        return self._x, self._y
    
    def size(self) -> Point:
        return self._w, self._h
    
    def sprite(self) -> str:
        return self._death_sprites[self._animation_index_death]
    
    def move(self, arena : Arena):
        if self._death_lenght <= 0:
            arena.kill(self)
        else:
            self._animation_counter_death = (self._animation_counter_death + 1) % 10 #rallentiamo il cambio di frame
            if self._animation_counter_death == 0:
                self._animation_index_death = (self._animation_index_death + 1) % len(self._death_sprites)
            self._death_lenght -= 1

class Ballom_Death(Actor):
    def __init__(self, pos: tuple):
        self._x, self._y = pos
        self._w, self._h = 32, 32
        self._death_sprites = ["png/ballom_death1.png","png/ballom_death1.png","png/ballom_death1.png","png/ballom_death1.png","png/ballom_death1.png","png/ballom_death1.png", "png/ballom_death2.png", "png/ballom_death3.png", "png/ballom_death4.png", "png/ballom_death5.png", "png/100.png", "png/100.png", "png/100.png", "png/100.png", "png/100.png"]
        self._death_lenght = 60
        self._animation_index_death = 0 
        self._animation_counter_death = 0

    def pos(self) -> Point:
        return self._x, self._y
    
    def size(self) -> Point:
        return self._w, self._h
    
    def sprite(self) -> str:
        return self._death_sprites[self._animation_index_death]
    
    def move(self, arena : Arena):
        if self._death_lenght <= 0:
            arena.kill(self)
        else:
            self._animation_counter_death = (self._animation_counter_death + 1) % 10 #rallentiamo il cambio di frame
            if self._animation_counter_death == 0:
                self._animation_index_death = (self._animation_index_death + 1) % len(self._death_sprites)

        self._death_lenght -= 1 #***

class Ballom(Actor):
    def __init__(self, pos: tuple, size=(32, 32)):
        self._x, self._y = pos
        self._w, self._h = size
        self._sprites = ["png/ballom1.png", "png/ballom2.png", "png/ballom3.png", "png/ballom4.png", "png/ballom5.png", "png/ballom6.png"]
        
        self._speed = 1  # Ridotta velocità di movimento
        self._direction = random.choice([(self._speed, 0), (-self._speed, 0), (0, self._speed), (0, -self._speed)])
        self._last_direction = None
        self._sprite_index = 0
        self._animation_timer = 0  # Contatore per l'animazione
        self._movement_timer = 0   # Contatore per il movimento
        self._animation_delay = 10  # Cambia sprite ogni 10 frame
        self._movement_delay = 0.5   # Muove il Ballom ogni 15 frame


    def pos(self) -> Point:
        return self._x, self._y
    
    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> str:
        # Rallenta il cambio di sprite basandosi sul contatore
        self._animation_timer += 1
        if self._animation_timer >= self._animation_delay:
            self._sprite_index = (self._sprite_index + 1) % len(self._sprites)
            self._animation_timer = 0  # Resetta il contatore
        return self._sprites[self._sprite_index]

    def move(self, arena: Arena):
        self._movement_timer += 1 # move è richiamata nella funzione tick 30 volte al secondo, aumentiamo dunque ad ogni chiamata il timer per il cambio di direzione
        if self._movement_timer < self._movement_delay: #controllo se il timer ha superato il limite impostato (10)
            return  # se non lo ha superato non facciamo nulla

        self._movement_timer = 0  # se lo ha superato resetiamo il contatore
        directions = [(self._speed, 0), (-self._speed, 0), (0, self._speed), (0, -self._speed)] #dichiariamo le possibili direzioni (le modificheremo piu avanti quindi è necessario ridichiararle)

        if self._last_direction: # rimuovo l'ultima direzione per evitare che il personaggio si blocchi
            opposite = (-self._last_direction[0], -self._last_direction[1]) #opposto delle precedenti
            directions.remove(opposite) #rimozine

        random.shuffle(directions) #mescoliamo le direzioni
        for dx, dy in directions:
            if self._can_move(arena, dx, dy): #per ogni direzione verifichiamo per qualesi può muovere
                self._x += dx
                self._y += dy
                self._last_direction = (dx, dy)  #aggiorniamo l'ultima direzione tentata
                self._direction = (dx, dy) #aggiorniamo la diirezione attuale
                return
        
        self._last_direction = None
            
    def _can_move(self, arena: Arena, dx: int, dy: int) -> bool:
        """controlla se la direzione scelta dalla funzione random è valida
           verificando la colisione con gli altri elementi dell'arena
        """
        temp_ballom = Ballom((self.pos()[0] + dx, self.pos()[1] + dy))
        for actor in arena.actors():
            if actor is not self:
                if isinstance(actor, (Wall, Destructible_Block, Bomb, Ballom)):
                    if check_overlap(actor, temp_ballom):
                        return False
                elif isinstance(actor,(Bombergirl, Bomberman)):
                    if check_overlap(actor, temp_ballom):
                        arena.spawn(Bomberman_Death(actor.pos()))
                        arena.kill(actor)
        return True

class Wall(Actor):
    def __init__(self, pos: tuple):
        self._x, self._y = pos
        self._w, self._h = 32, 32

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> str:
        return "png/muro.png"  

    def move(self, arena: Arena):
        pass

class bomb_esplosion(Actor):
    def __init__(self, pos: tuple):
        self._x, self._y = pos
        self._w, self._h = 96, 96
        self._sprites_explosion = ["png/esplosione1.png", "png/esplosione2.png", "png/esplosione3.png", "png/esplosione4.png"]
        self._animation_index_esplosione = 0
        self._animation_counter_esplosione = 0
        self._timer = 50

    def pos(self) -> Point:
        return self._x, self._y
    
    def size(self) -> Point:
        return self._w, self._h
    
    def sprite(self) -> str:
        return self._sprites_explosion[self._animation_index_esplosione]
    
    def move(self, arena: Arena):
        if self._timer <= 0:
            arena.kill(self)
        else:
            self._animation_counter_esplosione = (self._animation_counter_esplosione + 1) % 10
            if self._animation_counter_esplosione == 0:
                self._animation_index_esplosione = (self._animation_index_esplosione + 1) % len(self._sprites_explosion)

        self._timer -= 1
        
class Bomb(Actor):
    def __init__(self, pos: tuple, owner=None):
        self._x, self._y = pos
        self._w, self._h = 32, 32
        self._animation_index = 0
        self._animation_counter = 0
        self._animation_index_esplosione = 0
        self._animation_counter_esplosione = 0
        self._sprites = ["png/bomba1.png", "png/bomba2.png", "png/bomba3.png"]
        self._timer = 90
        self._owner = owner

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> str:
        return self._sprites[self._animation_index]

    def move(self, arena: Arena):
        self._animation_counter = (self._animation_counter + 1) % 10
        if self._animation_counter == 0:
            self._animation_index = (self._animation_index + 1) % len(self._sprites)

        self._timer -= 1
        if self._timer <= 0:
            self.explode(arena)
            self._animation_index_esplosione = 0
            self._animation_counter_esplosione = 0

    def explode(self, arena: Arena):
        # rimuovo la bomba dall'arena
        arena.kill(self)
        self._owner.esiste_bomba = False

        # posizioni della croce
        explosion_positions = [
            (self._x, self._y - 32),  # sopra
            (self._x - 32, self._y),  # sinistra
            (self._x, self._y),       # centro
            (self._x + 32, self._y),  # destra
            (self._x, self._y + 32)   # sotto
        ]

        for explosion_x, explosion_y in explosion_positions:
            for actor in arena.actors():
                temp_explosion = Bomb((explosion_x, explosion_y))
                if isinstance(actor, Destructible_Block):
                    block_x, block_y = actor.pos()
                    if block_x == explosion_x and block_y == explosion_y:
                        arena.spawn(Destructible_Block_Death((actor._x, actor._y)))
                        arena.kill(actor)  # Distruggi il blocco
                elif isinstance(actor, Ballom):
                    if check_overlap(actor, temp_explosion):
                        arena.spawn(Ballom_Death((actor._x, actor._y)))
                        arena.kill(actor)  # Uccidi il Ballom
                elif isinstance(actor, Bomberman):
                    if check_overlap(actor, temp_explosion):
                        arena.spawn(Bomberman_Death((actor._x, actor._y)))
                        arena.kill(actor)  # Uccidi il bomberman
                elif isinstance(actor, Bombergirl):
                    if check_overlap(actor, temp_explosion):
                        arena.spawn(Bombergirl_Death((actor._x, actor._y)))
                        arena.kill(actor)  # Uccidi bombergirl
                elif isinstance(actor, Iceman):
                    if check_overlap(actor, temp_explosion):
                        arena.spawn(Iceaman_Death((actor._x, actor._y)))
                        arena.kill(actor)  # Uccidi iceman

        # genera l'animazione dell'esplosione
        arena.spawn(bomb_esplosion((self._x - 32, self._y - 32)))


def drawplayerpaths():
    valid_values = [32, 96, 160, 224, 288, 352]
    for value in valid_values:
        g2d.set_color((255,0,0))
        g2d.draw_line((0, value + 16), (MAP_WIDTH, value + 16), 5)
    
    for i in range(32, MAP_WIDTH, 64):
        g2d.set_color((0,0,255))
        g2d.draw_line((i + 16, 0), (i + 16, MAP_WIDTH), 5)

class Bomberman(Actor):
    def __init__(self, pos : tuple):
        self._x, self._y = pos
        self._w, self._h = 32, 32
        self._sprites_su = ["png/su1.png", "png/su2.png", "png/su3.png"]
        self._sprites_giu = ["png/giu1.png", "png/giu2.png", "png/giu3.png"]
        self._sprites_dx = ["png/destra1.png", "png/destra2.png", "png/destra3.png"]
        self._sprites_sx = ["png/sinistra1.png", "png/sinistra2.png", "png/sinistra3.png"]
        self.indice_animazioni = 0
        self.animation_counter = 0
        self._speed = 2
        self.esiste_bomba = False

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def will_collide_with_block(self, x: int, y: int, arena: Arena):
        """controlla la collisione tra """
        bomberman_temp = Bomberman((x,y))
        for actor in arena.actors():
            if isinstance(actor, (Wall, Destructible_Block)):
                if check_overlap(actor, bomberman_temp):
                    return (actor.pos())
        return False 
    
    def controllo_allineamento_x(self, arena : Arena, block : tuple): #pixel di tolleranza per l'allineamento
        valid_values = [x for x in range(32,MAP_HEIGHT-32, 64)] #griglia di passaggi orizzontali possibili per il giocatore sull'asse y
        def get_difference(value): #specifichiamo la funzione per la distanza tra personaggio e passaggi per il confronto nella funzione min
            return abs(value - self._y)

        closest = min(valid_values, key=get_difference)
        #g2d.set_color((255,255,0))
        #g2d.draw_line((0, closest+16), (MAP_WIDTH, closest+16), 4)
        if self._y != closest and abs(self._y - closest) < ALIGNMENT_TOLERANCE: 
            if self._y < closest:
                self._y += 2
            else:
                self._y -= 2

    def controllo_allineamento_y(self, arena : Arena, block : tuple):
        # Lista dei valori consentiti (grid y positions)
        valid_values = [x for x in range(32, (MAP_WIDTH - 32) + 1, 64)]
        def get_difference(value): #specifichiamo la funzione per la distanza tra personaggio e passaggi per il confronto nella funzione min
            return abs(value - self._x)

        closest = min(valid_values, key=get_difference)
        #g2d.set_color((255,255,0))
        #g2d.draw_line((closest+16, 0), (closest+16, MAP_HEIGHT), 4)
        if self._x != closest and abs(self._x - closest) < ALIGNMENT_TOLERANCE:
            if self._x < closest:
                self._x += 2
            else:
                self._x -= 2
                
    def move(self, arena: Arena):
        new_x, new_y = self._x, self._y
        moved = ''
        if 'ArrowRight' in arena.current_keys():
            new_x = self._x + self._speed
            if not self.will_collide_with_block(new_x, self._y, arena):
                self._x = new_x
                self.animate(self._sprites_dx)
                moved = True
            else:
                self.controllo_allineamento_x(arena, self.will_collide_with_block(new_x, self._y, arena))

        elif 'ArrowLeft' in arena.current_keys():
            new_x = self._x - self._speed
            if not self.will_collide_with_block(new_x, self._y, arena):
                self._x = new_x
                self.animate(self._sprites_sx)
                moved = True
            else:
                self.controllo_allineamento_x(arena, self.will_collide_with_block(new_x, self._y, arena))

        elif 'ArrowUp' in arena.current_keys():
            new_y = self._y - self._speed
            if not self.will_collide_with_block(self._x, new_y, arena):
                self._y = new_y
                self.animate(self._sprites_su)
                moved = True
            else:
                self.controllo_allineamento_y(arena, self.will_collide_with_block(new_x, self._y, arena))

        elif 'ArrowDown' in arena.current_keys():
            new_y = self._y + self._speed
            if not self.will_collide_with_block(self._x, new_y, arena):
                self._y = new_y
                self.animate(self._sprites_giu)
                moved = True
            else:
                self.controllo_allineamento_y(arena, self.will_collide_with_block(new_x, self._y, arena))


        if 'Spacebar' in arena.current_keys() and not self.esiste_bomba:
            self.place_bomb(arena)
            print("bomba")

        if 'p' in arena.current_keys():
            drawplayerpaths()

        if not moved:
            g2d.draw_image(self._sprites_giu[0], (self._x, self._y))

        # Mantengo il Bomberman all'interno dei confini dell'arena
        full_w, full_h = arena.full_size()
        self._x = max(0, min(self._x, full_w - self._w))
        self._y = max(0, min(self._y, full_h - self._h))
        arena.scroll(self._x)

    def animate(self, sprites):
        if self.animation_counter == 0:
            self.indice_animazioni = (self.indice_animazioni + 1) % len(sprites)
        self.animation_counter = (self.animation_counter + 1) % 10
        g2d.draw_image(sprites[self.indice_animazioni], (self._x, self._y))

    def place_bomb(self, arena: Arena):
        """Piazza una bomba nella posizione attuale del Bomberman."""
        bomb_x = (self._x // 32) * 32
        bomb_y = (self._y // 32) * 32
        bomba = Bomb((bomb_x, bomb_y), owner=self)
        arena.spawn(bomba)
        self.esiste_bomba = True

class Bombergirl(Actor):
    def __init__(self, pos : tuple):
        self._x, self._y = pos
        self._w, self._h = 32, 32
        self._sprites_su = ["png/bf_su1.png", "png/bf_su2.png", "png/bf_su3.png"]
        self._sprites_giu = ["png/bf_giu1.png", "png/bf_giu2.png", "png/bf_giu3.png"]
        self._sprites_dx = ["png/bf_destra1.png", "png/bf_destra2.png", "png/bf_destra3.png"]
        self._sprites_sx = ["png/bf_sinistra1.png", "png/bf_sinistra2.png", "png/bf_sinistra3.png"]
        self.indice_animazioni = 0
        self.animation_counter = 0
        self._speed = 2
        self.esiste_bomba = False
        bomber_num = 0

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def will_collide_with_block(self, x: int, y: int, arena: Arena):
        """controlla la collisione tra """
        bomberman_temp = Bomberman((x,y))
        for actor in arena.actors():
            if isinstance(actor, (Wall, Destructible_Block)):
                if check_overlap(actor, bomberman_temp):
                    return (actor.pos())
        return False 

    def controllo_allineamento_x(self, arena : Arena, block : tuple):
         #pixel di tolleranza per l'allineamento
        valid_values = [x for x in range(32,MAP_HEIGHT-32, 64)] #griglia di passaggi orizzontali possibili per il giocatore sull'asse y
        def get_difference(value): #specifichiamo la funzione per la distanza tra personaggio e passaggi per il confronto nella funzione min
            return abs(value - self._y)

        closest = min(valid_values, key=get_difference)
        if self._y != closest and abs(self._y - closest) < ALIGNMENT_TOLERANCE:
            if self._y < closest:
                self._y += 2
            else:
                self._y -= 2

    def controllo_allineamento_y(self, arena : Arena, block : tuple):
        # Lista dei valori consentiti (grid y positions)
        valid_values = [x for x in range(32, (MAP_WIDTH - 32) + 1, 64)]
        def get_difference(value): #specifichiamo la funzione per la distanza tra personaggio e passaggi per il confronto nella funzione min
            return abs(value - self._x)

        closest = min(valid_values, key=get_difference)
        if self._x != closest and abs(self._x - closest) < ALIGNMENT_TOLERANCE:
            if self._x < closest:
                self._x += 2
            else:
                self._x -= 2
                
    def move(self, arena: Arena):
        new_x, new_y = self._x, self._y
        moved = ''
        if 'd' in arena.current_keys():
            new_x = self._x + self._speed
            if not self.will_collide_with_block(new_x, self._y, arena):
                self._x = new_x
                self.animate(self._sprites_dx)
                moved = True
            else:
                self.controllo_allineamento_x(arena, self.will_collide_with_block(new_x, self._y, arena))
                print("personaggio in posizza: ", self._x, self._y)
                print("collisione con il blocco", self.will_collide_with_block(new_x, self._y, arena))

        elif 'a' in arena.current_keys():
            new_x = self._x - self._speed
            if not self.will_collide_with_block(new_x, self._y, arena):
                self._x = new_x
                self.animate(self._sprites_sx)
                moved = True
            else:
                self.controllo_allineamento_x(arena, self.will_collide_with_block(new_x, self._y, arena))
                print("personaggio in posizza: ", self._x, self._y)
                print("collisione con il blocco", self.will_collide_with_block(new_x, self._y, arena))

        elif 'w' in arena.current_keys():
            new_y = self._y - self._speed
            if not self.will_collide_with_block(self._x, new_y, arena):
                self._y = new_y
                self.animate(self._sprites_su)
                moved = True
            else:
                self.controllo_allineamento_y(arena, self.will_collide_with_block(new_x, self._y, arena))
                print("personaggio in posizza: ", self._x, self._y)
                print("collisione con il blocco", self.will_collide_with_block(new_x, self._y, arena))

        elif 's' in arena.current_keys():
            new_y = self._y + self._speed
            if not self.will_collide_with_block(self._x, new_y, arena):
                self._y = new_y
                self.animate(self._sprites_giu)
                moved = True
            else:
                self.controllo_allineamento_y(arena, self.will_collide_with_block(new_x, self._y, arena))
                print("personaggio in posizza: ", self._x, self._y)
                print("collisione con il blocco", self.will_collide_with_block(new_x, self._y, arena))

        if 'x' in arena.current_keys() and not self.esiste_bomba:
            self.place_bomb(arena)
            print("bomba")

        if 'b' in arena.current_keys():
            drawplayerpaths()

        if not moved:
            g2d.draw_image(self._sprites_giu[0], (self._x, self._y))

        # Mantengo il Bomberman all'interno dei confini dell'arena
        full_w, full_h = arena.full_size()
        self._x = max(0, min(self._x, full_w - self._w))
        self._y = max(0, min(self._y, full_h - self._h))
        arena.scroll(self._x)

    def animate(self, sprites):
        if self.animation_counter == 0:
            self.indice_animazioni = (self.indice_animazioni + 1) % len(sprites)
        self.animation_counter = (self.animation_counter + 1) % 10
        g2d.draw_image(sprites[self.indice_animazioni], (self._x, self._y))

    def place_bomb(self, arena: Arena):
        """Piazza una bomba nella posizione attuale del Bomberman."""
        bomb_x = (self._x // 32) * 32
        bomb_y = (self._y // 32) * 32
        bomba = Bomb((bomb_x, bomb_y), owner=self)
        arena.spawn(bomba)
        self.esiste_bomba = True

class Destructible_Block(Actor):
    def __init__(self, pos : tuple):
        self._x, self._y = pos
        self._w, self._h = 32, 32  # Same size as permanent walls

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> str:
        return "png/blocco.png"

    def move(self, arena: Arena):
        pass  # Destroyable blocks are static until destroyed
class Iceman(Actor):
    def __init__(self, pos : tuple, size=(32, 32)):
        self._x, self._y = pos
        self._w, self._h = size
        self._sprites = ["png/iceman1.png", "png/iceman2.png", "png/iceman3.png", "png/iceman4.png", "png/iceman5.png", "png/iceman6.png"]
        
        self._speed = 1  # Ridotta velocità di movimento
        self._direction = random.choice([(self._speed, 0), (-self._speed, 0), (0, self._speed), (0, -self._speed)])
        self._last_direction = None
        self._sprite_index = 0
        self._animation_timer = 0  # Contatore per l'animazione
        self._movement_timer = 0   # Contatore per il movimento
        self._animation_delay = 10  # Cambia sprite ogni 10 frame
        self._movement_delay = 0.5   # Muove il Ballom ogni 15 frame


    def pos(self) -> Point:
        return self._x, self._y
    
    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> str:
        # Rallenta il cambio di sprite basandosi sul contatore
        self._animation_timer += 1
        if self._animation_timer >= self._animation_delay:
            self._sprite_index = (self._sprite_index + 1) % len(self._sprites)
            self._animation_timer = 0  # Resetta il contatore
        return self._sprites[self._sprite_index]

    def move(self, arena: Arena):
       # Rallenta il movimento basandosi sul contatore
        self._movement_timer += 1
        if self._movement_timer < self._movement_delay:
            return  # Non esegue il movimento finché non scade il timer

        self._movement_timer = 0  # Resetta il contatore
        directions = [(self._speed, 0), (-self._speed, 0), (0, self._speed), (0, -self._speed)]

        # Rimuovi la direzione opposta a quella appena tentata
        if self._last_direction:
            opposite = (-self._last_direction[0], -self._last_direction[1])
            directions.remove(opposite)

        # Mescola le direzioni e prova a muoverti
        random.shuffle(directions)
        for dx, dy in directions:
            if self._can_move(arena, dx, dy):
                self._x += dx
                self._y += dy
                self._last_direction = (dx, dy)  # Aggiorna la direzione tentata
                self._direction = (dx, dy)  # Aggiorna la direzione attuale
                return

        # Se nessuna direzione è valida, resta fermo
        self._last_direction = None  # Resetta l'ultima direzione 
        
    def _can_move(self, arena: Arena, dx: int, dy: int) -> bool:
        temp_iceman = Iceman((self.pos()[0] + dx, self.pos()[1] + dy))
        for actor in arena.actors():
            if actor is not self:
                if isinstance(actor, (Wall, Bomb, Ballom, Iceman)):
                    if check_overlap(actor, temp_iceman):
                        return False
        return True
class Iceaman_Death(Actor):
    def __init__(self, pos : tuple):
        self._x, self._y = pos
        self._w, self._h = 32, 32
        self._death_sprites = ["png/iceman_death.png", "png/200.png","png/200.png","png/200.png","png/200.png"]
        self._death_lenght = 60
        self._animation_index_death = 0
        self._animation_counter_death = 0
    def pos(self) -> Point:
        return self._x, self._y
    
    def size(self) -> Point:
        return self._w, self._h
    
    def sprite(self) -> str:
        return self._death_sprites[self._animation_index_death]
    
    def move(self, arena : Arena):
        if self._death_lenght <= 0:
            arena.kill(self)
        else:
            self._animation_counter_death = (self._animation_counter_death + 1) % 10 #rallentiamo il cambio di frame
            if self._animation_counter_death == 0:
                self._animation_index_death = (self._animation_index_death + 1) % len(self._death_sprites)
            self._death_lenght -= 1 #***