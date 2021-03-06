import matplotlib.pylab as plt
import robel_parser as rp
from makana_jimmy_program import position_library

import redis

vocab = position_library
vocab['muscle_combo_1'] = '(* (& muscle_flex_1 muscle_flex_2 muscle_flex_3 muscle_flex_4 muscle_flex_5 muscle_flex_6 muscle_flex_7) 0.5)'
vocab['muscle_combo_2'] = '(* (& muscle_flex_7 muscle_flex_6 muscle_flex_5 muscle_flex_4 muscle_flex_3 muscle_flex_2 muscle_flex_1) 0.5)'
vocab['combo_1'] = '(+ muscle_combo_1 muscle_combo_2)'
vocab['wave2'] = '(& wave2_1 wave2_2 wave2_3 wave2_4 wave2_5 wave2_6 wave2_7 stand)'
vocab['wave1'] = '(& wave_1 wave_2 wave_3 wave_4 wave_5 stand)'
# vocab['greeting'] = '(((wave_1 + wave_2) & (right_arm_down & left_arm_down)) * )'
vocab['greeting'] = '(& (+ (* wave1 1.6) (* wave2 1.6)) stand)'
vocab['onguard'] = '(& onguard_1 onguard_2 onguard_3 onguard_4 onguard_5 onguard_6 stand)'
vocab['why'] = '(& why_1 why_2 why_3 why_4 why_5 why_6 why_7 stand)'
vocab['jumping'] = '(& head_90_left head_90_right raise_arms hug)'
vocab['leila_dances'] = '(* (& head_40_right head_40_left raise_arms right_arm_wave left_arm_wave look_up) 0.8)'
vocab['police_freeze'] = '(& police_freeze_1 police_freeze_2 police_freeze_3 police_freeze_4 police_freeze_5 police_freeze_6 police_freeze_7 stand)'
vocab['muscle_flex'] = '(& muscle_flex_1 muscle_flex_2 muscle_flex_3 muscle_flex_4 muscle_flex_5 muscle_flex_6 muscle_flex_7 stand)'
vocab['yes'] = '(& yes_1 yes_2 yes_3 stand)'
vocab['wow'] = '(& wow_1 wow_2 wow_3 wow_4 stand)'
vocab['yawn'] = '(& yawn_1 yawn_2 yawn_3 stand)'
vocab['brah'] = '(& brah_1 brah_2 brah_3 brah_4 brah_5 brah_6 brah_7 stand)'
vocab['clap'] = '(& clap_1 clap_2 clap_3 clap_4 clap_5 clap_6 clap_7 stand)'
vocab['oops'] = '(& oops_1 oops_2 oops_3 oops_4 oops_5 oops_6 stand)'
vocab['search'] = '(& search_1 search_2 search_3 search_4 search_5 search_6 search_7 stand)'
vocab['wave3'] = '(& wave3_0 wave3_1 wave3_2 wave3_3 wave3_4 wave3_5 wave3_6 stand)'
vocab['jump1'] = '(& jump1_0 jump1_1 jump1_2 jump1_3 jump1_4 jump1_5 jump1_6 stand)'
vocab['pickupbox'] = '(& pickupbox_0 pickupbox_1 pickupbox_2 pickupbox_3 pickupbox_4 pickupbox_5 stand)'
vocab['victorypose'] = '(& victorypose_0 victorypose_1 victorypose_2 victorypose_3 victorypose_4 victorypose_5 victorypose_6 stand)'
vocab['victorypose_copy'] = '(& victorypose_copy1_0 victorypose_copy1_1 victorypose_copy1_2 victorypose_copy1_3 victorypose_copy1_4 victorypose_copy1_5 victorypose_copy1_6 stand)'
vocab['victorypose_long'] = '(& victorypose victorypose_copy (* victorypose_copy 0.6))'
vocab['wait_0'] = '(& wait_0_0 wait_0_1 wait_0_2 wait_0_3 wait_0_4 wait_0_5 wait_0_6 stand)'
vocab['wait_1'] = '(& wait_1_0 wait_1_1 wait_1_2 wait_1_3 wait_1_4 wait_1_5 stand)'
vocab['alas'] = '(& alas_0 alas_1 alas_2 alas_3 alas_4 alas_5 alas_6 stand)'
vocab['alas_mirror'] = '(& alas_mirror_0 alas_mirror_1 alas_mirror_2 alas_mirror_3 alas_mirror_4 alas_mirror_5 alas_mirror_6 stand)'
vocab['alas2'] = '(& alas_2_0 alas_2_1 alas_2_2 alas_2_3 alas_2_4 alas_2_5 alas_2_6 stand)'
vocab['nope'] = '(& nope_nope_0 nope_nope_1 nope_nope_2 nope_nope_3 nope_nope_4 nope_nope_5 nope_nope_6 stand)'
vocab['waiting'] = '(* (+ yawn nope wait_0 wait_1) 0.7)'

# Add new keys
rp.acts += vocab.keys()

def test_probabilities(exp, n=1000):
    d = {}
    for i in range(n):
        foo = rp.parsex(exp)
        # foo = len(foo.replace(' ',''))
        if foo in d.keys():
            d[foo] += 1
        else:
            d[foo] = 1
    # lists = sorted(d.items())
    # x, y = zip(*lists)  # unpack a list of pairs into two tuples
    # print x
    # print y
    # for a, b in zip(x, y):
    #     plt.text(a,b, str("%s\n%s" % (a, b)))
    plt.xlabel("String length")
    plt.ylabel("Occurence")
    plt.title("Union: %s P=0.3 N=1000" % exp)
    # plt.plot(x, y)

    # For bar chart (use on Union)
    # See for labeling: https://stackoverflow.com/a/30229062
    l = sorted(d.items())
    x, y = zip(*l)
    plt.bar(range(len(y)), y, align="center")
    plt.xticks(range(len(x)), x)

    plt.show()

# DEBUG=True

r = redis.StrictRedis(host="localhost", port=6379, db=0)
import time
import re
if __name__=='__main__':
    to_parse = '(* (& (+ left right) (+ up down right left) 0.75) 5.7)'
    wedge_to_parse = '(* (& up left down right) 5.7)'
    # to_parse = '(_ muscle_combo_1 oops waiting)'
    word = rp.parsex(to_parse)
    wedge = rp.parsex(wedge_to_parse)
    # ref: https://stackoverflow.com/a/26949785
    box = re.sub("\s+",",",word).split(',')
    wedge = re.sub("\s+",",",wedge).split(',')
    # for w in box:
    #     w = w.strip()
    #     print("Sending: %s" % w)
    #     r.publish('test', w)
    #     time.sleep(2)
    # r.publish('test', "end")
    for b, w in zip(box, wedge):
        b = b.strip()
        w = w.strip()
        print('Sending:\n   box: %s, wedge: %s' % (b, w))
        r.publish('test', b)
        r.publish('wedge', w)
        time.sleep(2)
    r.publish('test', 'end')
    r.publish('wedge', 'end')


    # x = test_probabilities(to_parse)
    # print x
    # rp.expand_sequence('(& waiting (+ oops wave3))', vocab)