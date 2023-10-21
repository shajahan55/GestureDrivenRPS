import cv2
import mediapipe as mp
from time import time, sleep
from math import hypot
from GestureDriverRPS import RockPaperScissor, Rock, Paper, Scissor

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

def update_scoreboard(scoreboard, rock_paper_scissor_drive:RockPaperScissor):
    # Draw the score values
    score1_text = f"{rock_paper_scissor_drive.player_one.name}: {rock_paper_scissor_drive.player_one.score}"
    score2_text = f"{rock_paper_scissor_drive.player_two.name}: {rock_paper_scissor_drive.player_two.score}"
    
    cv2.putText(scoreboard, score1_text, (30, 40), cv2.FONT_HERSHEY_PLAIN, 3, (0, 231, 123), 4, cv2.LINE_AA)
    cv2.putText(scoreboard, score2_text, (30, 90), cv2.FONT_HERSHEY_PLAIN, 3, (0, 231, 123), 4, cv2.LINE_AA)

def get_distance(hand_pos_dict:dict, tip1, tip2):
    print(tip1, tip2, hypot(hand_pos_dict[0][tip1].get('x') - hand_pos_dict[0][tip2].get('x'), hand_pos_dict[0][tip1].get('y') - hand_pos_dict[0][tip2].get('y')))
    return hypot(hand_pos_dict[0][tip1].get('x') - hand_pos_dict[0][tip2].get('x'), hand_pos_dict[0][tip1].get('y') - hand_pos_dict[0][tip2].get('y'))

def is_closed(hand_pos_dict, tip1, tip2):
    return True if get_distance(hand_pos_dict, tip1, tip2) <= 20 else False

def determine_choice(hand_pos_dict:dict) -> str:
    pinky_tip = 20
    ring_finger_tip = 16
    middle_finger_tip = 12
    index_finger_tip = 8
    thumb_finger_tip = 4

    if not is_closed(hand_pos_dict, middle_finger_tip, index_finger_tip): # Definetly not Rock if middle and index are open
        if is_closed(hand_pos_dict, pinky_tip, ring_finger_tip) and is_closed(hand_pos_dict, thumb_finger_tip, ring_finger_tip):
            return Scissor()
        return Paper()
    return Rock()

if __name__ == '__main__':
    player_one_name = input('Enter Name: ')
    rock_paper_scissor_drive = RockPaperScissor(player_one_name)
    overlay_image = cv2.imread('overlay.png')
    ongoing_countdown = False
    while True:
        success, img = cap.read()
        update_scoreboard(img, rock_paper_scissor_drive)
        if ongoing_countdown:
            cv2.putText(img, f'{rock_paper_scissor_drive.player_one.name} Chose {player_one_choice.element_name}', (30, 400), cv2.FONT_HERSHEY_PLAIN, 3, (0, 231, 123), 4, cv2.LINE_AA)
            cv2.putText(img, f'{rock_paper_scissor_drive.player_two.name} Chose {player_two_choice.element_name}', (30, 440), cv2.FONT_HERSHEY_PLAIN, 3, (0, 231, 123), 4, cv2.LINE_AA)
            if time() - countdown_time > 5:
                ongoing_countdown = False
        else:
            cv2.putText(img, 'Choose RPS', (30, 400), cv2.FONT_HERSHEY_PLAIN, 3, (0, 231, 123), 4, cv2.LINE_AA)
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)

            hand_pos_dict = dict()

            if results.multi_hand_landmarks:
                for idx, handLms in enumerate(results.multi_hand_landmarks):
                    hand_pos_dict[idx] = dict()
                    for id, lm in enumerate(handLms.landmark):
                        # print(id, lm)
                        h, w, c = img.shape
                        cx, cy = int(lm.x*w), int(lm.y*h)
                        pos_dict = dict(x=cx, y=cy)
                        hand_pos_dict[idx][id] = pos_dict

                    mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
                
                
                player_one_choice = determine_choice(hand_pos_dict)
                player_two_choice = rock_paper_scissor_drive.player_two.decide()
                # cv2.putText(img, str(int(fps)), (480, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)
                # cv2.putText(img, str(int(fps)), (480, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)
                rock_paper_scissor_drive.match(player_one_choice, player_two_choice)
                ongoing_countdown = True
                countdown_time = time()

        cTime = time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (480, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

        if rock_paper_scissor_drive.match_decided():
            if rock_paper_scissor_drive.player_one.won:
                winner = rock_paper_scissor_drive.player_one
                loser = rock_paper_scissor_drive.player_two
            else:
                winner = rock_paper_scissor_drive.player_two
                loser = rock_paper_scissor_drive.player_one
            cv2.putText(img, f'Result: {winner.name} Won {loser.name}', (30, 400), cv2.FONT_HERSHEY_PLAIN, 3, (0, 231, 123), 4, cv2.LINE_AA)  
            sleep(10)
            rock_paper_scissor_drive.result()
            break

    

