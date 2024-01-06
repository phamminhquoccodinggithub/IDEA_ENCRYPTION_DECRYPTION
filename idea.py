# pylint:disable=invalid-name
"""
    Main file to execute IDEA Encryption and Decryption
"""
#!/usr/bin/python python3

import random
import sys
import utils


def idea(block, key, mode='encryption'):
    """IDEA Encryption and Decryption

    Args:
        block (str): input data
        key (str): input key
        mode (str): encryption or decryption. Default is encryption

    Returns:
        str: Data after encryption or decryption
    """
    binaryData = block
    X = utils.split_into_x_parts_of_y(binaryData, 4, 16)
    print("Split (DHHUTECH): ", X)
    Z = utils.generate_subkeys(key)
    if mode == 'decryption':
        Z = utils.generate_decrypt_keys(Z)
    print("Key: (CAOHOCHUTECHCNTT)", key)
    print("-"*10)
    print(Z)
    #  8 Rounds
    for i in range(8):
        # variable names will follow the fourteen-step method
        # described in the document
        multiplier = i * 6

        one = utils.m_mul(X[0], Z[multiplier + 0])
        two = utils.m_sum(X[1], Z[multiplier + 1])
        three = utils.m_sum(X[2], Z[multiplier + 2])
        four = utils.m_mul(X[3], Z[multiplier + 3])
        five = utils.XOR(one, three)
        six = utils.XOR(two, four)
        seven = utils.m_mul(five, Z[multiplier + 4])
        eight = utils.m_sum(six, seven)
        nine = utils.m_mul(eight, Z[multiplier + 5])
        ten = utils.m_sum(seven, nine)
        eleven = utils.XOR(one, nine)
        twelve = utils.XOR(three, nine)
        thirteen = utils.XOR(two, ten)
        fourteen = utils.XOR(four, ten)
        print(f'Round {i+1}: ')
        print('Step one:', X[0], Z[multiplier + 0], one)
        print('Step two:', X[1], Z[multiplier + 1], two)
        print('Step three:', X[2], Z[multiplier + 2], three)
        print('Step four:', X[3], Z[multiplier + 3], four)
        print('Step five:', one, three, five)
        print('Step six:', two, four, six)
        print('Step seven:', five, Z[multiplier + 4], seven)
        print('Step eight:', six, seven, eight)
        print('Step nine:', eight, Z[multiplier + 5], nine)
        print('Step ten:', seven, nine, ten)
        print('Step eleven:', one, nine, eleven)
        print('Step twelve:', three, nine, twelve)
        print('Step thirteen:', two, ten, thirteen)
        print('Step fourteen:', four, ten, fourteen)
        if i == 7:
            X = [eleven, thirteen, twelve, fourteen]
        else:
            X = [eleven, twelve, thirteen, fourteen]
        print('X: ', X)

    # Output transformation (half-round)
    X[0] = utils.m_mul(X[0], Z[48])
    X[1] = utils.m_sum(X[1], Z[49])
    X[2] = utils.m_sum(X[2], Z[50])
    X[3] = utils.m_mul(X[3], Z[51])
    print(Z[48])
    print(Z[49])
    print(Z[50])
    print(Z[51])
    print('Output Transformation: ', X)
    return ''.join(X)


if __name__ == '__main__':
    # =============================
    #     Argument Handling
    # =============================
    args = sys.argv
    if len(args) < 3:
        Exception("mode, message")
    # mode_arg = args[1]
    # data = args[2]
    mode_arg = '-e'
    DATA = 'DHHUTECH'
    # DATA = '1011011011010010010011011000101111011010011100011011011100111100'
    mode = ""
    PRIVATE_KEY = "CAOHOCHUTECHCNTT"

    if mode_arg == "-e":
        mode = "encryption"
        data = utils.str_to_bits(DATA)
        # PRIVATE_KEY = int2bits(random.randint(1, pow(2, 128)))
    elif mode_arg == "-d":
        mode = "decryption"
        # PRIVATE_KEY = args[3]
    else:
        Exception("Incorrect parameter")
    private_key = utils.str_to_bits(PRIVATE_KEY, size=128)
    # =============================
    #     I.D.E.A
    # =============================
    result = idea(data, private_key, mode)

    # =============================
    #     Display
    # =============================
    if mode == "e":
        print("**********ENCRYPTION**********")
        print("Key: \t" + PRIVATE_KEY)
    else:
        print("**********DECRYPTION**********")
        result = utils.decode_binary_string(result)
    print('------------------------------------')
    print("Output:\t" + result)
    print('*'*30)
