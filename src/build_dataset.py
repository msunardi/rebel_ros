#!/usr/bin/env python
import rospy
import rosservice
from std_msgs.msg import String
from rebel_ros.srv import *
import ast
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import robel_parser as rp
from makana_jimmy_program import position_library

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
vocab['wait_2'] = '(& wait_2_0 wait_2_1 wait_2_2 wait_2_3 wait_2_4 wait_2_5 wait_2_6 stand)'
vocab['alas'] = '(& alas_0 alas_1 alas_2 alas_3 alas_4 alas_5 alas_6 stand)'
vocab['alas_mirror'] = '(& alas_mirror_0 alas_mirror_1 alas_mirror_2 alas_mirror_3 alas_mirror_4 alas_mirror_5 alas_mirror_6 stand)'
vocab['alas2'] = '(& alas_2_0 alas_2_1 alas_2_2 alas_2_3 alas_2_4 alas_2_5 alas_2_6 stand)'
vocab['nope'] = '(& nope_nope_0 nope_nope_1 nope_nope_2 nope_nope_3 nope_nope_4 nope_nope_5 nope_nope_6 stand)'
vocab['waiting'] = '(* (+ yawn nope wait_0 wait_1) 0.7)'
vocab['lookdownup'] = '(& lookdownup_1 lookdownup_2 lookdownup_3 lookdownup_4 lookdownup_5 lookdownup_6 lookdownup_7 stand)'

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
    plt.title("Union: %s P=/ N=1000" % exp)
    # plt.plot(x, y)

    # For bar chart (use on Union)
    # See for labeling: https://stackoverflow.com/a/30229062
    l = sorted(d.items())
    x, y = zip(*l)
    plt.bar(range(len(y)), y, align="center")
    plt.xticks(range(len(x)), x)

    plt.show()

DEBUG=True

def runner():
    
    rospy.wait_for_service('rebel_parser_server')
    rospy.init_node('datasetbuilder', anonymous=True)
    rate = rospy.Rate(10)
    rebel_parser = rospy.ServiceProxy('rebel_parser_server', Rebel)
    instances = {}
    while not rospy.is_shutdown():
        xinput = '(* (+ muscle_flex oops wave_1 wave_2 raise_arms right_arm_wave left_arm_wave right_handshake left_handshake head_40_left head_40_right hands_in_the_air_1 hands_in_the_air_2 police_freeze gasp onguard wow yes why brah search clap pickupbox victorypose victorypose_copy waiting wait_0 wait_1 wait_2 alas alas_mirror alas_2 nope) 2.7)'
        #poop = rosservice.call_service("rebel_parser_server", ["(+ muscle_flex oops)"])
        poop = rebel_parser(xinput)
        #rospy.loginfo(poop)
        
        try:
            poop_word = '-'.join([poo.replace('-','').replace(' ','') for poo in poop.word.split(' ') if poo != ''])
            if poop_word not in instances.keys():
                instances[poop_word] = poop.sequence
                # remove whitespaces from word
                poop_data = ast.literal_eval(poop.sequence)  # convert dict string to dict

                df = pd.DataFrame(data=poop_data)
                rospy.loginfo("[RUNNER] Writing new file: {}".format(poop_word))
                df.to_csv('./csv/{}.csv'.format(poop_word))
            else:
                rospy.loginfo("[RUNNER] word already known: {}".format(poop_word))
        except Exception as e:
            print("Something went wrong in saving data... {}".format(e))

        rate.sleep()

if __name__=='__main__':
    # to_parse = '(+ a b c d e 0.2)'
    # to_parse = '(~ muscle_combo_1 oops waiting)'
    # rp.parsex(to_parse)
    to_parse = ['(+ a b c d [0.5 0.1 0.2 0.2])', '(+ a b c d 0.4)', '(+ a b c d)', '(+ (& a b) c d [0.2 0.3 0.5])']
    # to_parse = ['(+ (& a b x y z 0.4) c d [0.2 0.3 0.5])']
    out = []
    # for i in range(100):
    #     for p in to_parse:
    #         out.append(rp.parsex(p))
    # print out
    # x = test_probabilities(to_parse[2])

    # rp.expand_sequence('(& waiting (+ oops wave3))', vocab)
    try:
        runner()
    except rospy.ROSInterruptException:
        pass
