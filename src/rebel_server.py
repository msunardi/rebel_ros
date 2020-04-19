#!/usr/bin/env python

from rebel_ros.srv import *
import robel_parser as rp
import rospy

import makana_jimmy_program as mjp

vocab = mjp.position_library
# vocab['muscle_combo_1'] = '((muscle_flex_1 & (muscle_flex_2 & (muscle_flex_3 & (muscle_flex_4 & (muscle_flex_5 & (muscle_flex_6 & muscle_flex_7)))))) * 0.5)'
# vocab['muscle_combo_2'] = '((muscle_flex_7 & (muscle_flex_6 & (muscle_flex_5 & (muscle_flex_4 & (muscle_flex_3 & (muscle_flex_2 & muscle_flex_1)))))) * 0.5)'
# vocab['combo_1'] = '(muscle_combo_1 + muscle_combo_2)'
# vocab['wave2'] = '((wave2_1 & (wave2_2 & (wave2_3 & (wave2_4 & (wave2_5 & (wave2_6 & wave2_7)))))) & stand)'
# vocab['wave1'] = '((wave_1 & (wave_2 & (wave_3 & (wave_4 & wave_5)))) & stand)'
# # vocab['greeting'] = '(((wave_1 + wave_2) & (right_arm_down & left_arm_down)) * )'
# vocab['greeting'] = '(((wave1 & (wave1 * 0.6)) + (wave2 & (wave2 * 0.6))) & stand)'
# vocab['onguard'] = '((onguard_1 & (onguard_2 & (onguard_3 & (onguard_4 & (onguard_5 & onguard_6 ))))) & stand)'
# vocab['why'] = '((why_1 & (why_2 & (why_3 & (why_4 & (why_5 & (why_6 & why_7)))))) & stand)'
# vocab['jumping'] = '(head_90_left & (head_90_right & (raise_arms & hug)))'
# vocab['leila_dances'] = '((head_40_right & (head_40_left & (raise_arms & (right_arm_wave & (left_arm_wave & look_up))))) * 0.8)'
# vocab['police_freeze'] = '((police_freeze_1 & (police_freeze_2 & (police_freeze_3 & (police_freeze_4 & (police_freeze_5 & (police_freeze_6 & police_freeze_7)))))) & stand)'
# vocab['muscle_flex'] = '((muscle_flex_1 & (muscle_flex_2 & (muscle_flex_3 & (muscle_flex_4 & (muscle_flex_5 & (muscle_flex_6 & muscle_flex_7)))))) & stand)'
# vocab['yes'] = '((yes_1 & (yes_2 & yes_3)) & stand)'
# vocab['wow'] = '((wow_1 & (wow_2 & (wow_3 & wow_4))) & stand)'
# vocab['yawn'] = '((yawn_1 & (yawn_2 & yawn_3)) & stand)'
# vocab['brah'] = '((brah_1 & (brah_2 & (brah_3 & (brah_4 & (brah_5 & (brah_6 & brah_7)))))) & stand)'
# vocab['clap'] = '((clap_1 & (clap_2 & (clap_3 & (clap_4 & (clap_5 & (clap_6 & clap_7)))))) & stand)'
# vocab['oops'] = '((oops_1 & (oops_2 & (oops_3 & (oops_4 & (oops_5 & oops_6))))) & stand)'
# vocab['search'] = '((search_1 & (search_2 & (search_3 & (search_4 & (search_5 & (search_6 & search_7)))))) & stand)'
# vocab['wave3'] = '((wave3_0 & (wave3_1 & (wave3_2 & (wave3_3 & (wave3_4 & (wave3_5 & wave3_6)))))) & stand)'
# vocab['jump1'] = '((jump1_0 & (jump1_1 & (jump1_2 & (jump1_3 & (jump1_4 & (jump1_5 & jump1_6)))))) & stand)'
# vocab['pickupbox'] = '((pickupbox_0 & (pickupbox_1 & (pickupbox_2 & (pickupbox_3 & (pickupbox_4 & pickupbox_5))))) & stand)'
# vocab['victorypose'] = '((victorypose_0 & (victorypose_1 & (victorypose_2 & (victorypose_3 & (victorypose_4 & (victorypose_5 & victorypose_6)))))) & stand)'
# vocab['victorypose_copy'] = '((victorypose_copy1_0 & (victorypose_copy1_1 & (victorypose_copy1_2 & (victorypose_copy1_3 & (victorypose_copy1_4 & (victorypose_copy1_5 & victorypose_copy1_6)))))) & stand)'
# vocab['victorypose_long'] = '(victorypose & (victorypose_copy & (victorypose_copy* 0.6)))'
# vocab['wait_0'] = '((wait_0_0 & (wait_0_1 & (wait_0_2 & (wait_0_3 & (wait_0_4 & (wait_0_5 & wait_0_6)))))) & stand)'
# vocab['wait_1'] = '((wait_1_0 & (wait_1_1 & (wait_1_2 & (wait_1_3 & (wait_1_4 & wait_1_5))))) & stand)'
# vocab['alas'] = '((alas_0 & (alas_1 & (alas_2 & (alas_3 & (alas_4 & (alas_5 & alas_6)))))) & stand)'
# vocab['alas_mirror'] = '((alas_mirror_0 & (alas_mirror_1 & (alas_mirror_2 & (alas_mirror_3 & (alas_mirror_4 & (alas_mirror_5 & alas_mirror_6)))))) & stand)'
# vocab['alas2'] = '((alas_2_0 & (alas_2_1 & (alas_2_2 & (alas_2_3 & (alas_2_4 & (alas_2_5 & alas_2_6)))))) & stand)'
# vocab['nope'] = '((nope_nope_0 & (nope_nope_1 & (nope_nope_2 & (nope_nope_3 & (nope_nope_4 & (nope_nope_5 & nope_nope_6)))))) & stand)'
# vocab['waiting'] = '((yawn + (nope + (wait_0 + wait_1))) * 0.7)'

vocab['muscle_combo_1'] = '(* (& stand muscle_flex_1 muscle_flex_2 muscle_flex_3 muscle_flex_4 muscle_flex_5 muscle_flex_6 muscle_flex_7 stand) 1.0)'
vocab['muscle_combo_2'] = '(* (& muscle_flex_7 muscle_flex_6 muscle_flex_5 muscle_flex_4 muscle_flex_3 muscle_flex_2 muscle_flex_1) 1.5)'
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
vocab['home'] = 'initial_stand'


# Add new keys
rp.acts += vocab.keys()
rp.Xvocab = vocab  # hack to make subtraction work
# rp.update_vocab(vocab.keys())

def parse(request):
    # Parse request
    # If expression, expand
    expression = request.expression
    # word = rp.eval(rp.parse(expression))
    # word = parsex(expression)
    sequence = []
    expansion = []
    sequence, expansion = rp.expand_sequence(expression, vocab, expansion)
    # If generic behavior name, choose a corresponding expression
    # print "Word: %s" % word

    # THIS IS A HACK! THE SEQUENCE WILL KEEP EXPANDING OTHERWISE
    # Still need to figure out why it is so

    # TODO: FIX THIS BUG!!!
    print("parse(): expansion: {}".format(expansion))
    print("parse(): sequence RAW: {}".format(sequence))
#    expansion_length = len(expansion[-1].split(" "))
#    sequence = sequence[-expansion_length:]
    print("Sequence [PRE]: %s" % sequence)

    # Return expanded string or sequence?

    # sequence = [vocab[k] for k in word.replace('\n','').replace('\r','').split( )]
    print("Sequence before JimmyDo: {}".format(sequence))
    sequence = mjp.JimmyDo(sequence)


    print("Evaluating expression: \"%s\" to: \"%s\"" % (expression, expansion))
    print("Sequence: %s" % sequence)

    # expansion = None
    # print expansion
    # response = ''
    # if len(expansion) > 0:
    #     for exp in expansion[1:]:
    #         response += str(exp)
    #         print("Response: {} (total: {})".format(response, len(expansion)))
    # for s, v in sequence:
    # 	print "%s: %s" % (s, v)
    return RebelResponse(expansion[0], str(sequence))
    # return {'word': response, 'sequence': sequence}

def rebel_server():
    rospy.init_node('rebel_parser_server')
    s = rospy.Service('rebel_parser_server', Rebel, parse)
    print("Ready to parse")
    rospy.spin()

if __name__ == "__main__":
    rebel_server()