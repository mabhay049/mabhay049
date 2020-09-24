from kivy.properties import NumericProperty,ReferenceListProperty,ObjectProperty
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.core.window import Window
from kivy.config import Config
from time import sleep
from random import randint

Window.size=(360,600)

class AirBall(Widget):
    velocity_x=NumericProperty(0)
    velocity_y=NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x,velocity_y)

    def move(self):
        self.pos=Vector(*self.velocity) + self.pos
class AirBorder(Widget):
    def bounce_ball(self,ball):
        if self.collide_widget(ball):
            ball.velocity_y *=-1

class AirBorderX(Widget):
    def bounce_back(self,ball):
        if self.collide_widget(ball):
            ball.velocity_x *= -1


class AirPaddle(Widget):
    score = NumericProperty(0)
    def hitback(self,ball):
        if self.collide_widget(ball):
            ball.velocity_y *= -1.001
            #self.remove_widget(ball)

class AirHockeyGame(Widget):
    ball = ObjectProperty(None)
    paddle1 = ObjectProperty(None)
    paddle2 = ObjectProperty(None)
    border1 = ObjectProperty(None)
    border2 = ObjectProperty(None)
    border3 = ObjectProperty(None)
    border4 = ObjectProperty(None)
    bod1 = ObjectProperty(None)
    bod2 = ObjectProperty(None)

    def serve_ball(self):
        self.ball.velocity = Vector(5,0).rotate(randint(0,360))

    def update(self,dt):
        self.ball.move()
        if (self.ball.y<-10):
            self.ball.velocity_y *= -1
            self.paddle2.score += 1

        if(self.ball.y>self.height-40):
            self.ball.velocity_y *= -1
            self.paddle1.score += 1

        self.border1.bounce_ball(self.ball)
        self.border2.bounce_ball(self.ball)
        self.border3.bounce_ball(self.ball)
        self.border4.bounce_ball(self.ball)

        self.bod1.bounce_back(self.ball)
        self.bod2.bounce_back(self.ball)

        self.paddle1.hitback(self.ball)
        self.paddle2.hitback(self.ball)



        #if self.ball.y > self.paddle1.y and self.ball.y < (self.paddle1.y + self.paddle1.height):
         #   self.ball.velocity_x *= -1
        #if self.ball.x > self.paddle1.x and self.ball.x < self.paddle1.x + self.paddle1.width:
         #   self.ball.velocity_y *= -1

        #if self.ball.y > self.paddle2.y and self.ball.y < (self.paddle2.y + self.paddle2.height):
            #self.ball.velocity_x *= -1
        #if self.ball.x > self.paddle2.x and self.ball.x < self.paddle2.x + self.paddle2.width:
            #self.ball.velocity_y *= -1

    def on_touch_move(self, touch):
        if (touch.y <= self.height/1/2.5):
            self.paddle1.center_y = touch.y
            self.paddle1.x = touch.x
        if (touch.y >= self.height/1/1.65):
            self.paddle2.center_y = touch.y
            self.paddle2.x = touch.x





class AirHockeyApp(App):
    def build(self):
        hockey=AirHockeyGame()
        hockey.serve_ball()
        Clock.schedule_interval(hockey.update,1.0/100.0)
        return(hockey)

AirHockeyApp().run()


