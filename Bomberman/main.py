from random import shuffle
from actor import *
from entità import *
import time

selected_option = 0
key_pressed = False
destructible_block = []
fixed_walls = []
occupied_positions = []

class BombermanGame(Arena):
    def __init__(self, size = (928,446), nPlayers = 1, nBalloms = 1, time = 160):
        super().__init__(size, size)
        self._nPlayers = nPlayers
        self._nBalloms = nBalloms
        self._time = time
        self._nPlayers = nPlayers
        self._game_state = "menu"
        self._game_level = 1
    
    def create_map(self):
        global destructible_block, fixed_walls
        width, height = self.full_size()
        block_size = 32 

        # controllo se è la prima volta che genero la mappa
        # creo i muri del bordo
        for x in range(0, 928, block_size):
            # muri orizzontali superiori e inferiori
            wall_sup = Wall((x, 0))
            wall_inf = Wall((x, 416 - block_size))
            self.spawn(wall_sup)
            self.spawn(wall_inf)
            fixed_walls.append((x, 0))
            fixed_walls.append((x, 416 - block_size))

        for y in range(0, 416, block_size):
            # muri verticali sinistri e destri
            wall_sx = Wall((0, y))
            wall_dx = Wall((928 - block_size, y))
            self.spawn(wall_sx)
            self.spawn(wall_dx)
            fixed_walls.append((0, y))
            fixed_walls.append((928 - block_size, y))

        # creo i muri interni
        for x in range(64, 928 - block_size, 64):
            for y in range(64, 416 - block_size, 64):
                wall = Wall((x, y))
                self.spawn(wall)
                fixed_walls.append((x, y))

        # creo il Bomberman se non esiste
        if not any(isinstance(actor, Bomberman) for actor in self.actors()):
            bomberman = Bomberman((32, 32))
            self.spawn(bomberman)
        if self._nPlayers == 2: # Se viene scelta la modalità in coppia spawno due bomberman
            bomberman2 = Bombergirl((32, 352))
            self.spawn(bomberman2)

        for actors in self.actors():
            print(actors)

        # mi creo una zona sicura in modo tale che il bomberman non rimanga incastrato allo spawn
        safe_zone = [(32, 32), (64, 32), (32, 64)] 
        safe_zone_2 = [(32, 32), (64, 32), (32, 64), (32, 352), (32, 320), (64, 352)] # creo la zona sicura per i due bomberman

        # se la lista dei blocchi distruggibili è vuota, la inizializzo
        posizioni_valide = []

        for y in range(block_size, height - block_size, block_size):
            for x in range(block_size, width - block_size, block_size):
                pos = (x, y)

                if self._nPlayers == 2:
                    # escludo la safe_zone 2 se i giocatori sono due e i muri fissi
                    if pos in safe_zone_2 or pos in fixed_walls:
                        continue
                    posizioni_valide.append(pos)
                else:
                    # sscludi la safe_zone e i muri fissi
                    if pos in safe_zone or pos in fixed_walls:
                        continue
                    posizioni_valide.append(pos)
                    
        # mescolo le posizioni e cre0 blocchi distruggibili
        shuffle(posizioni_valide)

        for pos in posizioni_valide[:40]:
            block = Destructible_Block(pos)
            occupied_positions.append(pos)
            self.spawn(block)
            destructible_block.append((block, pos))

        exit_door = Ddoor(posizioni_valide[5])
        self.spawn(exit_door)
        print(exit_door.pos())

        occupied_positions.append(fixed_walls) # aggiungo i muri fissi alla lista delle posizioni occupate

        valid_positions = posizioni_valide[20:]

        shuffle(valid_positions)
                
        for pos in valid_positions[:self._nBalloms]:
            ballom = Ballom(pos, size=(32, 32))  # Posiziona il Ballom su una posizione libera
            self.spawn(ballom)
            valid_positions.remove(pos) # Rimuovo le posizioni in cui vengono creati i ballom in modo tale  che gli iceman non vengano spawnati nello stesso punto
        if self._game_level > 1:
            for pos in valid_positions[:self._nBalloms - 4]:
                iceman = Iceman(pos, size=(32, 32))
                self.spawn(iceman)

    def draw_map(self):
        actors = self.actors()

        # separo le dverse categorie di attori
        exit_door = [actor for actor in actors if isinstance(actor, Ddoor)]
        walls = [actor for actor in actors if isinstance(actor, Wall)]
        destructible_blocks = [actor for actor in actors if isinstance(actor, Destructible_Block)]
        explosions = [actor for actor in actors if isinstance(actor, bomb_esplosion)]
        other_actors = [actor for actor in actors if not isinstance(actor, (bomb_esplosion, Wall, Destructible_Block, Ddoor))]

        # disegno prima la porta
        for actor in exit_door:
            g2d.draw_image(actor.sprite(), (actor.pos()[0] , actor.pos()[1]))

        # disegno l'esplosione
        for actor in explosions:
            g2d.draw_image(actor.sprite(), (actor.pos()[0], actor.pos()[1]))

        # disegno i muri fissi e quelli distruggibili
        for actor in walls + destructible_blocks:
            g2d.draw_image(actor.sprite(), (actor.pos()[0] , actor.pos()[1]))

        # disegno gli altri attori(Bomberman, nemici, etc.)
        for actor in other_actors:
            if not isinstance(actor, Bomberman) and not isinstance(actor, Bombergirl):
                g2d.draw_image(actor.sprite(), (actor.pos()[0] , actor.pos()[1]))


    def new_level(self, player):
        # quando passo ad un nuovo livello restto il tempo e aumento la variabile del livello
        player._time = 160
        player._level += 1
        self._game_level += 1
        g2d.set_color((0, 0, 0))
        g2d.draw_rect((0, 0), self.size())
        g2d.set_color((255, 255, 255))
        g2d.draw_text(f"Livello {player._level}", (self.size()[0] // 2, self.size()[1] // 2), 30)
        g2d.update_canvas()
        time.sleep(3)  # lascio aperto il canvas che mostra il livello per 3 secondi
        self.clear_map()
        self.create_map() # creo la nuova mappa per il nuovo livello

    def clear_map(self):
        for actor in self.actors():
            self.kill(actor)

    def draw_menu(self):
        # disegno il menu principale
        g2d.set_color((0, 0, 0))
        g2d.draw_rect((0, 0), self.size())

        g2d.set_color((0, 255, 0))
        g2d.draw_image("png/bomberman_title_screen.png", (164, 10))

        options = ["png/1_player_white.png", "png/1_player_yellow.png", "png/2_player_white.png", "png/2_player_yellow.png"]

        g2d.draw_image(options[0], ((arena_x / 10) + 20, arena_y - 120))
        g2d.draw_image(options[1], ((arena_x / 10) + 18, arena_y - 120))
        g2d.draw_image(options[2], ((arena_x / 1.6) + 20, arena_y - 120))
        g2d.draw_image(options[3], ((arena_x / 1.6) + 18, arena_y - 120))
        

        g2d.set_color((255,255,255))
        if selected_option == 1:
            g2d.draw_line(((arena_x / 1.6) + 20, arena_y - 60),((arena_x / 1.2) + 20, arena_y - 60), 5)
            g2d.draw_image('png/bomberman_main_menu.png', ((arena_x / 1.6) - 20, arena_y - 260))
            g2d.draw_image('png/bf_main_menu.png', ((arena_x / 1.3), arena_y - 260))
        else:
            g2d.draw_line(((arena_x / 10) + 20, arena_y - 60),((arena_x / 3.2) + 20, arena_y - 60), 5)
            g2d.draw_image('png/bomberman_main_menu.png', ((arena_x / 10) + 60, arena_y - 260))
    
    def restart_game(self, player: Giocatore):
        # Quando il bomberman muore ma ancora vite riprendo dal livello in cui è morto
        player._life -= 1
        player._time = 150
        player._bombergirl_alive = True
        player._bomberman_alive = True
        self.clear_map()
        g2d.set_color((0, 0, 0))
        g2d.draw_rect((0, 0), self.size())
        
        if player._life < 0:  # se ha fnito le vite e muore mostro la schermata di gameover
            g2d.set_color((255, 255, 0))
            g2d.draw_text("Game Over", (self.size()[0] // 2, self.size()[1] // 2 - 100), 50)
            g2d.set_color((255, 255, 255))
            g2d.draw_text(f"Nice try, you scored: {player.get_points()}", (self.size()[0] // 2, self.size()[1] // 2), 30)
            g2d.set_color((255, 255, 255))
            g2d.draw_text("Made with passion by Marco Ziveri and Lorenzo Gervasoni", (self.size()[0] // 2, self.size()[1] // 2 + 80), 30)
            print(self._game_state)
            g2d.update_canvas()
            time.sleep(10)   
            g2d.close_canvas()
        else:  
            g2d.set_color((255, 255, 255))
            g2d.draw_text(str(player._level), (self.size()[0] // 2, self.size()[1] // 2), 30)
            g2d.set_color((255, 255, 255))
            g2d.draw_text(f"Player Lives Left: {player._life}", (self.size()[0] // 2, self.size()[1] // 2 + 60), 30)
            g2d.update_canvas()
            time.sleep(3) 
            self._game_state = "gioco_singolo"  
            self.create_map()

    def avvio_gioco(self):
        for actor in self.actors():
            actor.move(self)


class BombermanGUI:
    def __init__(self):
        self._game = BombermanGame()
        self._player = Giocatore()
        self._game_state = self._game._game_state
        g2d.init_canvas(self._game.size())
        g2d.main_loop(self.tick)
       

    def tick(self):
        global arena_x, arena_y, key_pressed, selected_option
        arena_x = self._game._view_w
        arena_y = self._game._view_h
        self._player.check_timer() 
        # in base al game_state mostro la schermata
        if self._game_state == "menu": # schermata del menu
            self._player._points = 0
            self._player._time = 150
            self._game.draw_menu()
            keys = g2d.current_keys()
            if not key_pressed:
                if "ArrowRight" in keys:  # freccia destra
                    selected_option = (selected_option - 1) % 2  # uso il %2 in modo tale che se sono gia sulla prima opzione e clicco la freccia in su mi vada alla seconda opzione
                    key_pressed = True
                elif "ArrowLeft" in keys:  # freccia sinistra
                    selected_option = (selected_option + 1) % 2 # stesse identico ragionamento fatto sopra 
                    key_pressed = True
                elif "Enter" in keys:  # conferma selezione con il tasto invio
                    key_pressed = True
                    if selected_option == 0:  # modalità Singolo
                        self._game_state = "gioco_singolo"
                        self._game.create_map()
                    elif selected_option == 1:  # modalità Coppia
                        self._game._nPlayers = 2
                        self._game_state = "gioco_coppia"
                        self._game.create_map()
            else:
                if not keys:  # controllo sempre se viene cliccato qualche tasto
                    key_pressed = False

        elif self._game_state in ["gioco_singolo", "gioco_coppia"]:
            if self._player._level == 1:
                g2d.set_color((60,125,0))
            else:
                g2d.set_color(((self._player._level*100)%255, (self._player._level*100)%255, (self._player._level*50)%255))
            
            g2d.draw_rect((0, 0), (arena_x, arena_y - 30))
            keys = g2d.current_keys()
            self._game.tick(keys)

            door = [actor for actor in  self._game.actors() if isinstance(actor, Ddoor)]
            bmbman = [actor for actor in  self._game.actors() if isinstance(actor, Bomberman)]
            # la porta non è accessivbile se tutti i nemici non sono morti e il blocco distruggibile sopra la porta non è stato distrutto
            if door and self._player.check_for_win(self._game) == 0 and not any(isinstance(actor, Destructible_Block) and actor.pos() == door[0].pos() for actor in self._game.actors()):
                if check_collision(bmbman[0], door[0]) :
                    self._game.new_level(self._player)
                                
            if self._game_state != "":
                self._game.draw_map()
                self._game.avvio_gioco()
                self.draw_points()
                # aggiorno i punti dopo la morte dei ballom e degli iceman
                for actor in self._game.actors():
                    if isinstance(actor, Ballom_Death):
                        self._player._points += 3
                        self._player.check_for_win(self._game)
                    if isinstance(actor, Iceaman_Death):
                        self._player._points += 3
                        self._player.check_for_win(self._game)

            if self._game_state == "gioco_singolo":
                for actor in self._game.actors():
                    if not isinstance(actor, Bomberman) and isinstance(actor, Bomberman_Death): # se il bomberman muore restarto il game
                        self._game.restart_game(self._player)
            # se bomberman e bombergirl muoiono entrami restarto i lgame
            elif self._game_state == "gioco_coppia":
                for actor in self._game.actors():
                    if isinstance(actor, Bomberman_Death):
                        self._player._bomberman_alive = False
                    elif isinstance(actor, Bombergirl_Death):
                        self._player._bombergirl_alive = False
                if not self._player._bomberman_alive and not self._player._bombergirl_alive:
                    self._game.restart_game(self._player)

    # disegno la barra con le statistiche (punti, tempo e vite)
    def draw_points(self):
        arena_x = self._game._full_w
        arena_y = self._game._full_h
        player = self._player
        g2d.set_color((150, 150, 150))
        g2d.draw_rect((0, arena_y - 30), (arena_x, 30))
        g2d.set_color((0, 0, 0))
        g2d.draw_text(f"Time left: {player._time}", (60, arena_y - 18), 20)
        g2d.set_color((0, 0, 0))
        g2d.draw_text(f"Life: {player._life}", (10 + 200 + 10, arena_y - 18), 20)
        g2d.set_color((0, 0, 0))
        g2d.draw_text(f"Points: {str(player.get_points())}", (10 + 400 + 2 * 10, arena_y - 18), 20)
        g2d.set_color((0, 0, 0))
        g2d.draw_text(f"Left: {player.check_for_win(self._game)}", (10 + 600 + 2 * 10, arena_y - 18), 20)


if __name__ == "__main__":
    gui = BombermanGUI()