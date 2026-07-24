from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from direct.stdpy import thread
from player import Player
from monde import *
global P1, gun, cam, editor_camera

class MenuManager:
    def __init__(self):
        self.play_button = Button('Play', on_click=self.show_loading_screen)
        self.loading_screen = None

    def show_loading_screen(self):
        destroy(self.play_button)
        self.loading_screen = Entity(model='quad', texture='loading_image')
        thread.start_new_thread(function=self.load_level, args=())
        
    @staticmethod
    def setup_gameplay_ui(ski_physics):
        # Callback appelée à chaque bascule de la case
        def toggle_poles_mode():
            ski_physics.use_poles_mode = checkbox.value
            ski_physics.gravity = 12.0 if checkbox.value else 25.0

        checkbox = Checkbox(
            text=' Mode Bâtons',
            value=False,
            parent=camera.ui,
            position=(-0.7, 0.4),  # Ajuster selon votre disposition UI
            scale=0.1,
            z=-1,
        )
        checkbox.on_value_changed = toggle_poles_mode

    def load_level(self):
        global level, P1, gun
        level = Level()
        P1 = Player()  # Le joueur est une entité indépendante
        #gun = Entity(model='cube', parent=P1, position=(0.5, 0.25, 0.25), scale=(0.3, 0.2, 1), color=color.red)
        WManager = WorldManager(P1)
        destroy(self.loading_screen)
        self.setup_gameplay_ui(P1.physics)  # Passer l'instance de SkiPhysics du joueur à la fonction UI

# Instancié une seule fois à l'import de UI.py
pos_display = Text(
    text='',
    position=(-0.5, 0.45), # En haut à gauche de l'écran
    scale=0.7,
    color=color.yellow
)

_player_ref = None


# Fonction globale pour suivre le joueur avec la caméra
def update():
    global _player_ref
    
    # Recherche paresseuse (lazy search) du Player dans la scène s'il n'est pas encore trouvé
    if not _player_ref:
        for entity in scene.entities:
            if entity.__class__.__name__ == 'Player':
                _player_ref = entity
                break
    
    # Mise à jour si le joueur existe
    if _player_ref:
        pos = _player_ref.position
        suspension_height = _player_ref.physics.current_height if hasattr(_player_ref.physics, 'current_height') else -1
        pos_display.text = f"X: {pos.x:.1f} | Y: {pos.y:.1f} | Z: {pos.z:.1f} | Suspension: {suspension_height:.2f} | Poles Mode: {'ON' if _player_ref.physics.use_poles_mode else 'OFF'}"