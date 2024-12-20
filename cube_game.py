import sys
import pygame
import colour
import random
import asyncio
from bleak_eval_client import BleakEvalClient  # Import the client

sizeOfWindow = [1000, 750]
pygame.init()
win = pygame.display.set_mode(sizeOfWindow)
# Initialize BLE client (move this to be just a declaration)
bleak_client = None  # Will be initialized in main()

countOfEnemy = 5
randomSpead = True
randomColor = True
infinity = True
backgroundColor = (0, 0, 0)
enemiesList = []
running = True
score = 0
player = None
wave = 1
defaultStepWave = 20
stepWave = defaultStepWave
defaultLastWaveScore = 1
lastWaveScore = defaultLastWaveScore
gameOver = False
generateEnemy = True
playAgainR = None
quitR = None

iForWave = 0
startingTime = False
endFlagStartingTime = False
death_time = 0
is_dying = False
death_count = 0
in_intro = True
game_started = False


class ManagementGame:
    @staticmethod
    def init():
        global playAgainR, quitR, player
        player = Rect(100, 100, sizeOfWindow[0]//2 - 50, sizeOfWindow[1] - 150, "white", False, False, False, False, 8, 0, False, False)
        playAgainR = Rect(300, 200, 1450, 1000, "white", False, False, False, False, 0, 5, False, False)
        quitR = Rect(300, 200, 250, 1000, "white", False, False, False, False, 0, 5, False, False)

    @staticmethod
    async def gameOver(): # if you get hit
        global death_time, is_dying, death_count, bleak_client
        is_dying = True
        death_time = pygame.time.get_ticks()
        player.color = (255, 0, 0)
        death_count += 1 # increase the death count
        
        # Try to send bluetooth message if client exists
        try:
            if bleak_client:
                print('sent a message that we died')
                await bleak_client.send_message("Died")
        except Exception as e:
            print(f"Bluetooth communication failed: {e}")
        
        pygame.display.update()
        ManagementGame.claerEnemy()
        print('you just died')

    @staticmethod
    def showTitle(score):
        global wave
        textScore = pygame.font.Font(None, 80)
        win.blit(textScore.render(f"Score: {score}", False, (255, 255, 255)), (0, 0))
        textScore = pygame.font.Font(None, 60)
        win.blit(textScore.render(f"Wave: {wave}", False, (0, 0, 255)), (0, 60))
        textDeaths = pygame.font.Font(None, 60)
        win.blit(textDeaths.render(f"Deaths: {death_count}", False, (255, 0, 0)), (0, 120))
        if gameOver:
            ManagementGame.GameOverTitle()

    @staticmethod
    def GameOverTitle():
        global playAgainR
        global quitR
        global player
        global running
        global generateEnemy
        global gameOver
        global wave
        global lastWaveScore
        global score
        global defaultStepWave
        global defaultStepWave
        global stepWave
        text = pygame.font.Font(None, 250)
        text2 = pygame.font.Font(None, 100)
        win.blit(text.render(f"GAME OVER", False, (255, 0, 0)), (460, 650))
        win.blit(text2.render(f"final score: {score}", False, (255, 255, 255)), (720, 850))
        global playAgainR
        global quitR
        playAgainR.show()
        quitR.show()
        if (playAgainR.x < player.x < playAgainR.x + playAgainR.w) or (
                player.x < playAgainR.x < player.x + player.w) or (player.x == playAgainR.x):
            if (playAgainR.y < player.y < playAgainR.y + playAgainR.h) or (
                    player.y < playAgainR.y < player.y + player.h):
                running = True
                generateEnemy = True
                gameOver = False
                lastWaveScore = defaultLastWaveScore
                stepWave = defaultStepWave
                score = 0
                wave = 1

        if (quitR.x < player.x < quitR.x + quitR.w) or (player.x < quitR.x < player.x + player.w) or (
                player.x == quitR.x):
            if (quitR.y < player.y < quitR.y + quitR.h) or (player.y < quitR.y < player.y + player.h):
                pygame.quit()
                sys.exit()
        playAgainT = pygame.font.Font(None, 100)
        quitT = pygame.font.Font(None, 100)
        win.blit(playAgainT.render(f"again", False, (255, 255, 255)), (1510, 1060))
        win.blit(quitT.render(f"quit", False, (255, 255, 255)), (330, 1060))

    @staticmethod
    def claerEnemy():
        enemiesList.clear()
        player.x = sizeOfWindow[0]//2 - 50
        player.y = sizeOfWindow[1] - 150

    @staticmethod
    def manageWave():
        global lastWaveScore
        global stepWave
        global generateEnemy
        global wave
        global showTitleWave
        global startingTime
        global running
        global endFlagStartingTime
        global countOfEnemy
        if ((score - lastWaveScore) - stepWave) > 0:
            lastWaveScore = score
            wave += 1
            countOfEnemy += 2
            stepWave += countOfEnemy * 2
            startingTime = True
            running = False
            ManagementGame.claerEnemy()
        ManagementGame.checkTime(1000)
        if endFlagStartingTime and not gameOver:
            generateEnemy = True
            running = True
            endFlagStartingTime = False

        if startingTime:
            textWave = pygame.font.Font(None, 80)
            win.blit(textWave.render(f"Wave: {wave}", False, (255, 255, 255)), (450, 650))

    @staticmethod
    def checkTime(count):
        global iForWave
        global startingTime
        global endFlagStartingTime
        iForWave += 1
        if iForWave - count == 0:
            iForWave = 0
            startingTime = False
            endFlagStartingTime = True
            return True
        return False

    @staticmethod
    def showSensorData(bleak_client):
        try:
            # Create font object (do this once at initialization if possible)
            font = pygame.font.Font(None, 24)
            
            # Format sensor data strings
            gyro_text = f"Gyro: {bleak_client.gyro_x:.2f}, {bleak_client.gyro_y:.2f}, {bleak_client.gyro_z:.2f}"

            
            # Render text
            gyro_surface = font.render(gyro_text, True, (255, 255, 255))

            # Position text in upper right corner
            win.blit(gyro_surface, (sizeOfWindow[0] - gyro_surface.get_width() - 10, 30))
        except Exception as e:
            pass  # Silently fail if sensor data isn't available

    @staticmethod
    async def intoWhile():
        global is_dying, death_time
        
        ManagementGame.showTitle(score)
        ManagementGame.manageWave()
        
        ManagementGame.showSensorData(bleak_client)
        
        if is_dying:
            current_time = pygame.time.get_ticks()
            if current_time - death_time >= 500:
                is_dying = False
                player.color = (255, 255, 255)
                player.x = sizeOfWindow[0]//2 - 50
                player.y = sizeOfWindow[1] - 150
                ManagementGame.claerEnemy()
        
        # use delay to control the speeds, you can use arrows or gyro
        pygame.time.delay(5)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.moveY(False)
        if keys[pygame.K_DOWN]:
            player.moveY()
        if keys[pygame.K_LEFT]:
            player.moveX(False)
        if keys[pygame.K_RIGHT]:
            player.moveX()
        # end if

        # Handle gyroscope input
        try:
            # Get gyroscope data from bleak_eval_client
            # Assuming gyro_x and gyro_y are the pitch and roll angles
            gyro_x = bleak_client.gyro_x  # You'll need to adjust this based on your actual data structure
            gyro_y = bleak_client.gyro_y

            # Define threshold angles for movement
            threshold = 0.1  # Adjust this value to change sensitivity

            # Move based on gyroscope angles
            if gyro_x > threshold:
                player.moveY()  # Move down
            elif gyro_x < -threshold:
                player.moveY(False)  # Move up

            if gyro_y > threshold:
                player.moveX()  # Move right
            elif gyro_y < -threshold:
                player.moveX(False)  # Move left
        except:
            # If gyroscope data isn't available, continue with just keyboard controls
            pass
            # Handle gyroscope input
            try:
                # Get gyroscope data from bleak_eval_client
                # Assuming gyro_x and gyro_y are the pitch and roll angles
                gyro_x = bleak_client.gyro_x  # You'll need to adjust this based on your actual data structure
                gyro_y = bleak_client.gyro_y

                # Define threshold angles for movement
                threshold = 10  # Adjust this value to change sensitivity

                # Move based on gyroscope angles
                if gyro_x > threshold:
                    player.moveY()  # Move down
                elif gyro_x < -threshold:
                    player.moveY(False)  # Move up

                if gyro_y > threshold:
                    player.moveX()  # Move right
                elif gyro_y < -threshold:
                    player.moveX(False)  # Move left
            except:
                # If gyroscope data isn't available, continue with just keyboard controls
                pass

        ManagementGame.checkPlayer()
        player.show()
        
        if running:
            if generateEnemy:
                if len(enemiesList) < countOfEnemy:
                    Rect()
            for item in enemiesList:
                item.moveY()
                await item.check()
                
        pygame.display.update()
        win.fill(backgroundColor)

    @staticmethod
    def checkPlayer():
        global player
        if player.x + player.w > sizeOfWindow[0]:
            player.x = sizeOfWindow[0] - player.w
        if player.x < 0:
            player.x = 0
        if player.y < 0:
            player.y = 0
        if player.y + player.h > sizeOfWindow[1]:
            player.y = sizeOfWindow[1] - player.h

    @staticmethod
    def show_intro_screen():
        win.fill(backgroundColor)
        title_font = pygame.font.Font(None, 150)
        subtitle_font = pygame.font.Font(None, 80)
        
        # Draw title
        title_text = title_font.render("CUBE GAME", False, (255, 255, 255))
        title_rect = title_text.get_rect(center=(sizeOfWindow[0] // 2, sizeOfWindow[1] // 2 - 100))
        win.blit(title_text, title_rect)
        
        # Draw "Press SPACE to start" message
        start_text = subtitle_font.render("Press SPACE to start", False, (255, 255, 255))
        start_rect = start_text.get_rect(center=(sizeOfWindow[0] // 2, sizeOfWindow[1] // 2 + 100))
        win.blit(start_text, start_rect)
        
        pygame.display.update()


class Color:
    colorRGB = None
    nameOfSomeColor = ['DarkGreen', 'Green', 'DarkCyan', 'DeepSkyBlue', 'DarkTurquoise', 'MediumSpringGreen', 'Lime',
                       'SpringGreen', 'Cyan', 'Aqua', 'MidnightBlue', 'DodgerBlue', 'LightSeaGreen', 'ForestGreen',
                       'SeaGreen', 'DarkSlateGray', 'DarkSlateGrey', 'LimeGreen', 'MediumSeaGreen', 'Turquoise',
                       'RoyalBlue', 'SteelBlue', 'DarkSlateBlue', 'MediumTurquoise']

    def __init__(self, color="white"):
        self.getRGB(color)

    def getRGB(self, color):
        c = list(colour.Color(color).get_rgb())
        c[0] = int(c[0] * 255)
        c[1] = int(c[1] * 255)
        c[2] = int(c[2] * 255)
        self.colorRGB = tuple(c)

    def getColor(self):
        return self.colorRGB

    def getRandomColor(self):
        self.getRGB(random.choice(self.nameOfSomeColor))


class Rect:
    x = None
    y = None
    w = None
    h = None
    color = None
    spead = None
    border = None
    randColor = None
    randSize = None
    randPositionX = None
    randSpead = None
    randBorder = None
    is_player = None

    def __init__(self, w=0, h=0, x=0, y=0, color="white", randColor=True, randSize=True, randPositionX=True,
                 randSpead=True, spead=1,
                 border=5, append=True, randBorder=True):
        self.randColor = randColor
        self.x = x
        self.y = y
        self.spead = spead
        self.color = color
        self.border = border
        self.randSize = randSize
        self.w = w
        self.h = h
        self.randPositionX = randPositionX
        self.randSpead = randSpead
        self.randBorder = randBorder
        self.random()
        self.show()
        self.is_player = not append

        if append:
            enemiesList.append(self)

    def moveY(self, direction=True):
        if direction:
            self.y += self.spead
            self.show()
            self.destroyer()
        else:
            self.y -= self.spead
            self.show()
            self.destroyer()

    def random(self):
        if self.randColor:
            color = Color()
            color.getRandomColor()
            self.color = color.colorRGB
        if self.randSize:
            self.w = random.randint(30, 150)
            self.h = random.randint(30, 150)
        if self.randPositionX:
            self.x = random.randint(0, sizeOfWindow[0])
        if self.randSpead:
            self.spead = random.randint(1, 4)
        if self.randBorder:
            if random.randint(0, 1):
                self.border = random.randint(4, 15)
            else:
                self.border = 0

    def moveX(self, direction=True):
        if direction:
            self.x += self.spead
            self.show()
            self.destroyer()
        else:
            self.x -= self.spead
            self.show()
            self.destroyer()

    def show(self):
        pygame.draw.rect(win, self.color, ((self.x, self.y), (self.w, self.h)), self.border)

    def destroyer(self):
        if not self.is_player:
            if self.y > (sizeOfWindow[1] + 200):
                if self in enemiesList:
                    enemiesList.remove(self)
                    global score
                    score += 1

    async def check(self):
        if (self.x < player.x < self.x + self.w) or (player.x < self.x < player.x + player.w) or (player.x == self.x):
            if (self.y < player.y < self.y + self.h) or (player.y < self.y < player.y + player.h):
                await ManagementGame.gameOver()


async def main():
    global in_intro, game_started, bleak_client

    # Initialize BLE client once at startup
    try:
        bleak_client = BleakEvalClient()
        connected = await bleak_client.connect()
        if connected:
            print("Successfully connected to Bluetooth device")
        else:
            print("Could not connect to Bluetooth device - continuing without BLE")
    except Exception as e:
        print(f"Bluetooth initialization failed: {e}")
        bleak_client = None

    try:
        while True:
            if in_intro:
                ManagementGame.show_intro_screen()
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        raise SystemExit
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            in_intro = False
                            game_started = True
                            ManagementGame.init()
            else:
                await ManagementGame.intoWhile()
                events = pygame.event.get()
                for item in events:
                    if item.type == pygame.QUIT:
                        raise SystemExit
            
            await asyncio.sleep(0.01)
    finally:
        # Clean up Bluetooth connection when exiting
        try:
            if bleak_client:
                await bleak_client.disconnect()
        except:
            pass
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pygame.quit()
        sys.exit()
