from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            if (ball.top == self.y) or (ball.y == self.x):
                ball.velocity_y *= -1
            else:
                vx, vy = ball.velocity
                offset = (ball.center_y - self.center_y) / (self.height / 2)
                bounced = Vector(-1 * vx, vy)
                vel = bounced * 1.1
                ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):

    # Velocity of the ball on x and y axis
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    # Referencelist property so we can use ball.velocity as
    # a shorthand, just like e.g. w.pos for w.x and w.y
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # ``move`` function will move the ball one step. This
    # will be called in equal intervals to animate the ball
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    # Put back paddles and ball to default position
    def serve_ball(self, vel=(4, 0)):
        self.ids.win_title.height = '0dp'
        self.ball.center = self.center
        self.ball.velocity = vel
        self.player1.center_y = self.center_y
        self.player2.center_y = self.center_y

    # Start game again
    def reset(self, instance):
        self.remove_widget(self.reset_bt)
        self.add_widget(self.ids.label_left)
        self.add_widget(self.ids.label_right)
        Clock.schedule_interval(self.update, 1.0/60.0)

    # dt mean Delta Time
    def update(self, dt):
        # Check if player score reach maximum
        if (self.player1.score >= 1) or (self.player2.score >= 1):
            text = 'Player ' + ('1' if self.player1.score > self.player2.score else '2') + ' win!'
            self.ids.win_title.size_hint_y = 1
            self.ids.win_title.text = text
            self.remove_widget(self.ids.label_left)
            self.remove_widget(self.ids.label_right)
            self.reset_bt = Button(text='RESET', font_size=70, center_x=self.width, top=self.top*2/3-10)
            self.reset_bt.bind(on_press=self.reset)
            self.add_widget(self.reset_bt)
            return False

        # Else keep on update other functions
        self.ball.move()

        # Bound of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # Bound off top and bottom
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        # Went of to a side to score point?
        if self.ball.x < 0:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.right > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    # Move paddles
    def on_touch_move(self, touch):
        if (touch.x < self.width / 3) and (self.player1.top < self.height or self.player1.y > 0):
            self.player1.center_y = touch.y
        if (touch.x > self.width - self.width / 3) and (self.player2.top < self.height or self.player2.y > 0):
            self.player2.center_y = touch.y


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game


if __name__ == '__main__':
    PongApp().run()
