from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Rectangle
from kivy.clock import Clock
import random


class SpaceGame(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.enemies = []
        self.bullets = []

        self.game_over = False
        self.score = 0

        # Lives
        self.lives = 3

        # Enemy speed
        self.enemy_speed = 200

        # Bullet speed
        self.bullet_speed = 500

        # Enemies in each bunch
        self.enemy_count = 3

        # Last score milestone
        self.last_score_milestone = 0

        # Background
        with self.canvas.before:
            self.bg = Rectangle(
                source="space.png",
                pos=self.pos,
                size=self.size
            )

        self.bind(
            pos=self.update_bg,
            size=self.update_bg
        )

        # Player
        self.player = Image(
            source="player.jpg",
            size=(350, 350),
            pos=(200, 50)
        )

        self.add_widget(self.player)

        # Score
        self.score_label = Label(
            text="Score: 0",
            font_size="22sp",
            size=(150, 50),
            pos=(800, 370)
        )

        self.add_widget(self.score_label)

        # Lives
        self.lives_label = Label(
            text="Lives: 3",
            font_size="22sp",
            size=(150, 50),
            pos=(70, 370)
        )

        self.add_widget(self.lives_label)

        # Spawn enemies every 2 seconds
        Clock.schedule_interval(
            self.spawn_enemy,
            2
        )

        # Move enemies
        Clock.schedule_interval(
            self.move_enemies,
            1 / 60
        )

        # Auto fire
        Clock.schedule_interval(
            self.shoot,
            0.3
        )

        # Move bullets
        Clock.schedule_interval(
            self.move_bullets,
            1 / 60
        )

        # Enemy speed +50 every 8 seconds
        Clock.schedule_interval(
            self.increase_speed,
            8
        )

        # Bullet speed +60 every 2 seconds
        Clock.schedule_interval(
            self.increase_bullet_speed,
            2
        )

        # Enemy bunch +1 every 20 seconds
        Clock.schedule_interval(
            self.increase_enemy_count,
            20
        )

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    # ORIGINAL PLAYER MOVEMENT
    def on_touch_move(self, touch):

        if self.game_over:
            return True

        if self.player.collide_point(*touch.pos):
            self.player.center_x = touch.x
            return True

        return super().on_touch_move(touch)

    # Increase enemy speed
    def increase_speed(self, dt):

        if not self.game_over:
            self.enemy_speed += 50

    # Increase bullet speed
    def increase_bullet_speed(self, dt):

        if not self.game_over:
            self.bullet_speed += 60

    # Increase enemy bunch every 20 seconds
    def increase_enemy_count(self, dt):

        if not self.game_over:
            self.enemy_count += 1

    # Auto shoot
    def shoot(self, dt):

        if self.game_over:
            return

        bullet = Image(
            source="bullet.png",
            size=(30, 30)
        )

        bullet.center_x = self.player.center_x
        bullet.y = self.player.top

        self.add_widget(bullet)
        self.bullets.append(bullet)

    # Spawn enemies
    def spawn_enemy(self, dt):

        if self.game_over:
            return

        for i in range(self.enemy_count):

            enemy = Image(
                source="enemy.jpg",
                size=(100, 70)
            )

            enemy.x = random.randint(
                0,
                max(
                    0,
                    int(self.width - enemy.width)
                )
            )

            enemy.y = (
                self.height +
                random.randint(0, 300)
            )

            self.add_widget(enemy)
            self.enemies.append(enemy)

    # Move enemies
    def move_enemies(self, dt):

        if self.game_over:
            return

        for enemy in self.enemies[:]:

            enemy.y -= self.enemy_speed * dt

            # Enemy escaped
            if enemy.top < 0:

                if enemy in self.enemies:
                    self.enemies.remove(enemy)

                if enemy.parent:
                    self.remove_widget(enemy)

                self.lives -= 1

                self.lives_label.text = (
                    "Lives: " + str(self.lives)
                )

                # Game Over
                if self.lives <= 0:
                    self.show_game_over()
                    return

    # Move bullets
    def move_bullets(self, dt):

        if self.game_over:
            return

        for bullet in self.bullets[:]:

            bullet.y += self.bullet_speed * dt

            # Bullet leaves screen
            if bullet.y > self.height:

                if bullet in self.bullets:
                    self.bullets.remove(bullet)

                if bullet.parent:
                    self.remove_widget(bullet)

                continue

            # Collision
            for enemy in self.enemies[:]:

                if bullet.collide_widget(enemy):

                    if bullet in self.bullets:
                        self.bullets.remove(bullet)

                    if bullet.parent:
                        self.remove_widget(bullet)

                    if enemy in self.enemies:
                        self.enemies.remove(enemy)

                    if enemy.parent:
                        self.remove_widget(enemy)

                    self.score += 1

                    self.score_label.text = (
                        "Score: " + str(self.score)
                    )

                    # Increase bunch at
                    # score 200, 400, 600...
                    milestone = (
                        self.score // 200
                    ) * 200

                    if (
                        milestone > 0
                        and milestone >
                        self.last_score_milestone
                    ):
                        self.enemy_count += 1
                        self.last_score_milestone = milestone

                    break

    # Game Over
    def show_game_over(self):

        if self.game_over:
            return

        self.game_over = True

        # Remove player
        if self.player.parent:
            self.remove_widget(self.player)

        # Remove enemies
        for enemy in self.enemies[:]:

            if enemy.parent:
                self.remove_widget(enemy)

        self.enemies.clear()

        # Remove bullets
        for bullet in self.bullets[:]:

            if bullet.parent:
                self.remove_widget(bullet)

        self.bullets.clear()

        # Game Over text
        self.game_over_label = Label(
            text="GAME OVER",
            font_size="45sp",
            size=(400, 80),
            pos=(400, 800)
        )

        self.add_widget(
            self.game_over_label
        )

        # Final score
        self.final_score = Label(
            text="Score: " + str(self.score),
            font_size="25sp",
            size=(300, 50),
            pos=(500, 1000)
        )

        self.add_widget(
            self.final_score
        )

        # Red restart button
        self.restart_button = Button(
            text="RESTART",
            font_size="22sp",
            color=(0, 0, 0, 1),
            background_normal="",
            background_down="",
            background_color=(1, 0, 0, 1),
            size=(200, 70),
            pos=(500, 1000)
        )

        self.restart_button.bind(
            on_press=self.restart_game
        )

        self.add_widget(
            self.restart_button
        )

    # Restart game
    def restart_game(self, instance):

        self.remove_widget(
            self.game_over_label
        )

        self.remove_widget(
            self.final_score
        )

        self.remove_widget(
            self.restart_button
        )

        self.game_over = False
        self.score = 0

        # IMPORTANT:
        # Enemy speed is NOT reset.
        # Bullet speed is NOT reset.
        # Enemy count is NOT reset.

        # Reset lives
        self.lives = 3

        self.lives_label.text = "Lives: 3"
        self.score_label.text = "Score: 0"

        # New player
        self.player = Image(
            source="player.jpg",
            size=(350, 350),
            pos=(200, 50)
        )

        self.add_widget(
            self.player
        )


class SpaceShooterApp(App):

    def build(self):
        return SpaceGame()


SpaceShooterApp().run()