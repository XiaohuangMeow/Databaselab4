import ExtMem
from b_plus_tree import *
from basic import generateRS
from basic import write_r_to_disk
from basic import write_s_to_disk
from basic import print_R_S


def liner_selection(buffer):
    num = 0
    for i in range(16):
        addr = "r" + str(i)
        n = buffer.readBlockFromDisk(addr)
        for j in range(7):
            a = int(buffer.data[n][2 * j])
            b = int(buffer.data[n][2 * j + 1])
            if (a == 40):
                print("Relation_R", a, b)
                num += 1
                # buffer.writeBlockToDisk("liner_selection_result_R"+str(cnt),cnt)
                buffer.data[1].append(a)
                buffer.data[1].append(b)
                if num % 7 == 0:
                    buffer.writeBlockToDisk("liner_selection_result_R" + str((num - 1) // 7), 1)
                    buffer.freeBlockInBuffer(1)
        buffer.freeBlockInBuffer(n)
    if num % 7 != 0:
        buffer.writeBlockToDisk("liner_selection_result_R" + str((num - 1) // 7), 1)
        buffer.freeBlockInBuffer(1)
    num = 0
    for i in range(32):
        addr = "s" + str(i)
        n = buffer.readBlockFromDisk(addr)
        for j in range(7):
            c = int(buffer.data[n][2 * j])
            d = int(buffer.data[n][2 * j + 1])
            if (c == 60):
                print("Relation_S", c, d)
                num += 1
                buffer.data[1].append(c)
                buffer.data[1].append(d)
                if num % 7 == 0:
                    buffer.writeBlockToDisk("liner_selection_result_S" + str((num - 1) // 7), 1)
                    buffer.freeBlockInBuffer(1)
        buffer.freeBlockInBuffer(n)
    if num % 7 != 0:
        buffer.writeBlockToDisk("liner_selection_result_S" + str((num - 1) // 7), 1)
        buffer.freeBlockInBuffer(1)


# x=0-55
def get_buffer_data(buffer, x):
    return int(buffer.data[x // 7][2 * (x % 7)])


def swap_buffer_data(buffer, b1, d1, b2, d2):
    t1 = buffer.data[b2][d2 * 2]
    t2 = buffer.data[b2][d2 * 2 + 1]
    buffer.data[b2][d2 * 2] = buffer.data[b1][d1 * 2]
    buffer.data[b2][d2 * 2 + 1] = buffer.data[b1][d1 * 2 + 1]
    buffer.data[b1][d1 * 2] = t1
    buffer.data[b1][d1 * 2 + 1] = t2


def sort_buffer(buffer):
    for i in range(55):
        for j in range(55 - i):
            if int(get_buffer_data(buffer, j)) > int(get_buffer_data(buffer, j + 1)):
                swap_buffer_data(buffer, j // 7, j % 7, (j + 1) // 7, (j + 1) % 7)


def lower_bound(buffer, key, first, len):
    while len > 0:
        half = len // 2
        middle = first + half
        if get_buffer_data(buffer, middle) < key:
            first = middle + 1
            len = len - half - 1
        else:
            len = half
    return first


def merge_sort_R(buffer):
    for i in range(8):
        buffer.freeBlockInBuffer(i)
    # r1
    for i in range(8):
        buffer.readBlockFromDisk("r" + str(i))
    sort_buffer(buffer);
    for i in range(8):
        buffer.writeBlockToDisk("sort_R" + str(i), i)
    # r2
    for i in range(8, 16):
        buffer.readBlockFromDisk("r" + str(i))
    sort_buffer(buffer)
    for i in range(8):
        buffer.writeBlockToDisk("sort_R" + str(i + 8), i)
    # merge sort R
    cnt = 0
    f1 = 0
    f2 = 0
    i = 0
    j = 0
    b1 = buffer.readBlockFromDisk("sort_R" + str(f1))
    b2 = buffer.readBlockFromDisk("sort_R" + str(f2 + 8))
    n = buffer.getNewBlockInBuffer()
    result_num = 0
    while f1 != 8 and f2 != 8:
        if int(buffer.data[b1][2 * i]) < int(buffer.data[b2][2 * j]):
            a = buffer.data[b1][2 * i]
            b = buffer.data[b1][2 * i + 1]
            i += 1
        else:
            a = buffer.data[b2][2 * j]
            b = buffer.data[b2][2 * j + 1]
            j += 1
        buffer.data[n].append(a)
        buffer.data[n].append(b)
        cnt += 1
        if i == 7:
            f1 += 1
            i = 0
            if f1 < 8:
                buffer.freeBlockInBuffer(b1)
                b1 = buffer.readBlockFromDisk("sort_R" + str(f1))
        if j == 7:
            f2 += 1
            j = 0
            if f2 < 8:
                buffer.freeBlockInBuffer(b2)
                b2 = buffer.readBlockFromDisk("sort_R" + str(f2 + 8))
        if cnt % 7 == 0:
            buffer.writeBlockToDisk("binary_selection_temp_R" + str(result_num), n)
            n = buffer.getNewBlockInBuffer()
            result_num += 1
    if f1 == 8:
        while f2 != 8:
            a = buffer.data[b2][2 * j]
            b = buffer.data[b2][2 * j + 1]
            buffer.data[n].append(a)
            buffer.data[n].append(b)
            j += 1
            cnt += 1
            if j == 7:
                f2 += 1
                j = 0
                if f2 < 8:
                    buffer.freeBlockInBuffer(b2)
                    b2 = buffer.readBlockFromDisk("sort_R" + str(f2 + 8))
            if cnt % 7 == 0:
                buffer.writeBlockToDisk("binary_selection_temp_R" + str(result_num), n)
                n = buffer.getNewBlockInBuffer()
                result_num += 1
    elif f2 == 8:
        while f1 != 8:
            a = buffer.data[b1][2 * i]
            b = buffer.data[b1][2 * i + 1]
            buffer.data[n].append(a)
            buffer.data[n].append(b)
            i += 1
            cnt += 1
            if i == 7:
                f1 += 1
                i = 0
                if f1 < 8:
                    buffer.freeBlockInBuffer(b1)
                    b1 = buffer.readBlockFromDisk("sort_R" + str(f1))
            if cnt % 7 == 0:
                buffer.writeBlockToDisk("binary_selection_temp_R" + str(result_num), n)
                n = buffer.getNewBlockInBuffer()
                result_num += 1
    for i in range(8):
        buffer.freeBlockInBuffer(i)


def binary_search_R(buffer):
    key = 40
    cnt = 0
    result_num = 0
    for i in range(4):
        buffer.getNewBlockInBuffer()
    n = buffer.getNewBlockInBuffer()
    for k in range(4):
        for i in range(4):
            buffer.freeBlockInBuffer(i)
            buffer.readBlockFromDisk("binary_selection_temp_R" + str(4 * k + i))
        if key > get_buffer_data(buffer, 27) or key < get_buffer_data(buffer, 0):
            continue
        first = 0
        len = 28
        l1 = lower_bound(buffer, 40, first, len)
        l2 = lower_bound(buffer, 41, first, len)
        for i in range(l1, l2):
            a = buffer.data[i // 7][2 * (i % 7)]
            b = buffer.data[i // 7][2 * (i % 7) + 1]
            buffer.data[n].append(a)
            buffer.data[n].append(b)
            print("Relation_R", a, b)
            cnt += 1
            if cnt % 7 == 0:
                buffer.writeBlockToDisk("binary_selection_result_R" + str(result_num), n)
                result_num += 1
                n = buffer.getNewBlockInBuffer()
    if cnt % 7 != 0:
        buffer.writeBlockToDisk("binary_selection_result_R" + str(result_num), n)
    for i in range(8):
        buffer.freeBlockInBuffer(i)


def temp_merge_S(buffer, p1, p2, result_num):
    cnt = 0
    f1 = 0
    f2 = 0
    i = 0
    j = 0
    b1 = buffer.readBlockFromDisk("sort_S" + str(f1 + p1))
    b2 = buffer.readBlockFromDisk("sort_S" + str(f2 + p2))
    n = buffer.getNewBlockInBuffer()
    while f1 != 8 and f2 != 8:
        if int(buffer.data[b1][2 * i]) < int(buffer.data[b2][2 * j]):
            a = buffer.data[b1][2 * i]
            b = buffer.data[b1][2 * i + 1]
            i += 1
        else:
            a = buffer.data[b2][2 * j]
            b = buffer.data[b2][2 * j + 1]
            j += 1
        buffer.data[n].append(a)
        buffer.data[n].append(b)
        cnt += 1
        if i == 7:
            f1 += 1
            i = 0
            if f1 < 8:
                buffer.freeBlockInBuffer(b1)
                b1 = buffer.readBlockFromDisk("sort_S" + str(f1 + p1))
        if j == 7:
            f2 += 1
            j = 0
            if f2 < 8:
                buffer.freeBlockInBuffer(b2)
                b2 = buffer.readBlockFromDisk("sort_S" + str(f2 + p2))
        if cnt % 7 == 0:
            buffer.writeBlockToDisk("binary_selection_temp_S" + str(result_num), n)
            n = buffer.getNewBlockInBuffer()
            result_num += 1
    if f1 == 8:
        while f2 != 8:
            a = buffer.data[b2][2 * j]
            b = buffer.data[b2][2 * j + 1]
            buffer.data[n].append(a)
            buffer.data[n].append(b)
            j += 1
            cnt += 1
            if j == 7:
                f2 += 1
                j = 0
                if f2 < 8:
                    buffer.freeBlockInBuffer(b2)
                    b2 = buffer.readBlockFromDisk("sort_S" + str(f2 + p2))
            if cnt % 7 == 0:
                buffer.writeBlockToDisk("binary_selection_temp_S" + str(result_num), n)
                n = buffer.getNewBlockInBuffer()
                result_num += 1
    elif f2 == 8:
        while f1 != 8:
            a = buffer.data[b1][2 * i]
            b = buffer.data[b1][2 * i + 1]
            buffer.data[n].append(a)
            buffer.data[n].append(b)
            i += 1
            cnt += 1
            if i == 7:
                f1 += 1
                i = 0
                if f1 < 8:
                    buffer.freeBlockInBuffer(b1)
                    b1 = buffer.readBlockFromDisk("sort_S" + str(f1 + p1))
            if cnt % 7 == 0:
                buffer.writeBlockToDisk("binary_selection_temp_S" + str(result_num), n)
                n = buffer.getNewBlockInBuffer()
                result_num += 1
    for i in range(8):
        buffer.freeBlockInBuffer(i)


def merge_sort_S(buffer):
    for i in range(8):
        buffer.freeBlockInBuffer(i)
    # s1
    for i in range(8):
        buffer.readBlockFromDisk("s" + str(i))
    sort_buffer(buffer);
    for i in range(8):
        buffer.writeBlockToDisk("sort_S" + str(i), i)
    # s2
    for i in range(8, 16):
        buffer.readBlockFromDisk("s" + str(i))
    sort_buffer(buffer)
    for i in range(8):
        buffer.writeBlockToDisk("sort_S" + str(i + 8), i)
    # s3
    for i in range(16, 24):
        buffer.readBlockFromDisk("s" + str(i))
    sort_buffer(buffer);
    for i in range(8):
        buffer.writeBlockToDisk("sort_S" + str(i + 16), i)
    # s4
    for i in range(24, 32):
        buffer.readBlockFromDisk("s" + str(i))
    sort_buffer(buffer)
    for i in range(8):
        buffer.writeBlockToDisk("sort_S" + str(i + 24), i)
    # merge sort S
    temp_merge_S(buffer, 0, 8, 0)  # 0-16
    temp_merge_S(buffer, 16, 24, 16)  # 16-24
    result_num = 0
    cnt = 0
    f1 = 0
    f2 = 0
    i = 0
    j = 0
    b1 = buffer.readBlockFromDisk("binary_selection_temp_S" + str(f1))
    b2 = buffer.readBlockFromDisk("binary_selection_temp_S" + str(f2 + 16))
    n = buffer.getNewBlockInBuffer()
    while f1 != 16 and f2 != 16:
        if int(buffer.data[b1][2 * i]) < int(buffer.data[b2][2 * j]):
            a = buffer.data[b1][2 * i]
            b = buffer.data[b1][2 * i + 1]
            i += 1
        else:
            a = buffer.data[b2][2 * j]
            b = buffer.data[b2][2 * j + 1]
            j += 1
        buffer.data[n].append(a)
        buffer.data[n].append(b)
        cnt += 1
        if i == 7:
            f1 += 1
            i = 0
            if f1 < 16:
                buffer.freeBlockInBuffer(b1)
                b1 = buffer.readBlockFromDisk("binary_selection_temp_S" + str(f1))
        if j == 7:
            f2 += 1
            j = 0
            if f2 < 16:
                buffer.freeBlockInBuffer(b2)
                b2 = buffer.readBlockFromDisk("binary_selection_temp_S" + str(f2 + 16))
        if cnt % 7 == 0:
            buffer.writeBlockToDisk("binary_selection_temp2_S" + str(result_num), n)
            n = buffer.getNewBlockInBuffer()
            result_num += 1
    if f1 == 16:
        while f2 != 16:
            a = buffer.data[b2][2 * j]
            b = buffer.data[b2][2 * j + 1]
            buffer.data[n].append(a)
            buffer.data[n].append(b)
            j += 1
            cnt += 1
            if j == 7:
                f2 += 1
                j = 0
                if f2 < 16:
                    buffer.freeBlockInBuffer(b2)
                    b2 = buffer.readBlockFromDisk("binary_selection_temp_S" + str(f2 + 16))
            if cnt % 7 == 0:
                buffer.writeBlockToDisk("binary_selection_temp2_S" + str(result_num), n)
                n = buffer.getNewBlockInBuffer()
                result_num += 1
    elif f2 == 16:
        while f1 != 16:
            a = buffer.data[b1][2 * i]
            b = buffer.data[b1][2 * i + 1]
            buffer.data[n].append(a)
            buffer.data[n].append(b)
            i += 1
            cnt += 1
            if i == 7:
                f1 += 1
                i = 0
                if f1 < 16:
                    buffer.freeBlockInBuffer(b1)
                    b1 = buffer.readBlockFromDisk("binary_selection_temp_S" + str(f1))
            if cnt % 7 == 0:
                buffer.writeBlockToDisk("binary_selection_temp2_S" + str(result_num), n)
                n = buffer.getNewBlockInBuffer()
                result_num += 1
    for i in range(8):
        buffer.freeBlockInBuffer(i)


def binary_search_S(buffer):
    key = 60
    cnt = 0
    result_num = 0
    for i in range(4):
        buffer.getNewBlockInBuffer()
    n = buffer.getNewBlockInBuffer()
    for k in range(8):
        for i in range(4):
            buffer.freeBlockInBuffer(i)
            buffer.readBlockFromDisk("binary_selection_temp2_S" + str(4 * k + i))
        if key > get_buffer_data(buffer, 27) or key < get_buffer_data(buffer, 0):
            continue
        first = 0
        len = 28
        l1 = lower_bound(buffer, key, first, len)
        l2 = lower_bound(buffer, key + 1, first, len)
        for i in range(l1, l2):
            a = buffer.data[i // 7][2 * (i % 7)]
            b = buffer.data[i // 7][2 * (i % 7) + 1]
            buffer.data[n].append(a)
            buffer.data[n].append(b)
            print("Relation_S", a, b)
            cnt += 1
            if cnt % 7 == 0:
                buffer.writeBlockToDisk("binary_selection_result_S" + str(result_num), n)
                result_num += 1
                n = buffer.getNewBlockInBuffer()
    if cnt % 7 != 0:
        buffer.writeBlockToDisk("binary_selection_result_S" + str(result_num), n)
    for i in range(8):
        buffer.freeBlockInBuffer(i)


def binary_selection(buffer):
    merge_sort_R(buffer)
    binary_search_R(buffer)
    merge_sort_S(buffer)
    binary_search_S(buffer)
    for i in range(16):
        ExtMem.dropBlockOnDisk("sort_R" + str(i))
    for i in range(32):
        ExtMem.dropBlockOnDisk("sort_S" + str(i))
    for i in range(16):
        ExtMem.dropBlockOnDisk("binary_selection_temp_R" + str(i))
    for i in range(32):
        ExtMem.dropBlockOnDisk("binary_selection_temp_S" + str(i))
        ExtMem.dropBlockOnDisk("binary_selection_temp2_S" + str(i))

    # for i in range(32):
    #     if i < 8:
    #         buffer3.readBlockFromDisk("s" + str(i))
    #     elif i < 16:
    #         buffer4.readBlockFromDisk("r" + str(i))
    #     elif i < 24:
    #         buffer5.readBlockFromDisk("r" + str(i))
    #     elif i < 32:
    #         buffer6.readBlockFromDisk("r" + str(i))


def construct_b_plus_tree_R(buffer):
    tree = BPlusTree(order=4)
    for i in range(16):
        n = buffer.readBlockFromDisk("r" + str(i))
        for j in range(7):
            key = int(buffer.data[n][2 * j])
            value = (i, j)
            tree.insert(key, value)
        buffer.freeBlockInBuffer(n)
    return tree


def construct_b_plus_tree_S(buffer):
    tree = BPlusTree(order=4)
    for i in range(32):
        n = buffer.readBlockFromDisk("s" + str(i))
        for j in range(7):
            key = int(buffer.data[n][2 * j])
            value = (i, j)
            tree.insert(key, value)
        buffer.freeBlockInBuffer(n)
    return tree


def b_plus_tree_selection(buffer):
    tree = construct_b_plus_tree_R(buffer)
    list = tree.retrieve(40)
    cnt = 0
    m = buffer.getNewBlockInBuffer()
    for i, item in enumerate(list):
        x = item[0]
        y = item[1]
        n = buffer.readBlockFromDisk("r" + str(x))
        attr1 = buffer.data[n][2 * y]
        attr2 = buffer.data[n][2 * y + 1]
        print("Relation_R", attr1, attr2)
        buffer.data[m].append(attr1)
        buffer.data[m].append(attr2)
        cnt += 1
        buffer.freeBlockInBuffer(n)
        if cnt % 7 == 0:
            buffer.writeBlockToDisk("bplus_tree_index_result_R" + str((cnt - 1) // 7), m)
            m = buffer.getNewBlockInBuffer()
    if cnt % 7 != 0:
        buffer.writeBlockToDisk("bplus_tree_index_result_R" + str((cnt - 1) // 7), m)
    tree = construct_b_plus_tree_S(buffer)
    list = tree.retrieve(60)
    cnt = 0
    m = buffer.getNewBlockInBuffer()
    for i, item in enumerate(list):
        x = item[0]
        y = item[1]
        n = buffer.readBlockFromDisk("s" + str(x))
        attr1 = buffer.data[n][2 * y]
        attr2 = buffer.data[n][2 * y + 1]
        print("Relation_R", attr1, attr2)
        buffer.data[m].append(attr1)
        buffer.data[m].append(attr2)
        cnt += 1
        buffer.freeBlockInBuffer(n)
        if cnt % 7 == 0:
            buffer.writeBlockToDisk("bplus_tree_index_result_S" + str((cnt - 1) // 7), m)
            m = buffer.getNewBlockInBuffer()
    if cnt % 7 != 0:
        buffer.writeBlockToDisk("bplus_tree_index_result_S" + str((cnt - 1) // 7), m)
    for i in range(8):
        buffer.freeBlockInBuffer(i)


def project(buffer, relation, attribute):
    if attribute == 'A' or attribute == 'a' or attribute == 'C' or attribute == 'c':
        index_attribute = 0
    else:
        index_attribute = 1
    if relation == 'R':
        num = 16
        begin = "r"
    else:
        num = 32
        begin = "s"
    cnt = 0
    n = buffer.getNewBlockInBuffer()
    for i in range(num):
        m = buffer.readBlockFromDisk(begin + str(i))
        for j in range(7):
            attr = buffer.data[m][2 * j + index_attribute]
            buffer.data[n].append(attr)
            print("Project:" + relation, "Attribute:" + attribute, attr)
            cnt += 1
        buffer.freeBlockInBuffer(m)
        if cnt % 14 == 0:
            buffer.writeBlockToDisk("project" + str((cnt - 1) // 14), n)
            n = buffer.getNewBlockInBuffer()


def nest_loop_join(buffer):
    cnt = 0
    k = buffer.getNewBlockInBuffer()
    arr_num = buffer.numFreeBlk - 1
    for i in range(16 // arr_num + 1):
        for x in range(arr_num):
            buffer.freeBlockInBuffer(x+1)
        mlist = []
        for l in range(arr_num):
            if i * 6 + l < 16:
                m = int(buffer.readBlockFromDisk("r" + str(i * 6 + l)))
                mlist.append(m)
        for j in range(32):
            n = buffer.readBlockFromDisk("s" + str(j))
            # print(i, k,mlist,n)
            for m in mlist:
                for ii in range(7):
                    for jj in range(7):
                        # print(m)
                        if buffer.data[m][ii * 2] == buffer.data[n][jj * 2]:
                            # print(i,j,m,ii,jj)
                            a = buffer.data[m][ii * 2]
                            b = buffer.data[m][ii * 2 + 1]
                            c = buffer.data[n][jj * 2]
                            d = buffer.data[n][jj * 2 + 1]
                            print(a, b, c, d)
                            buffer.data[k].append(a)
                            buffer.data[k].append(b)
                            buffer.data[k].append(c)
                            buffer.data[k].append(d)
                            cnt += 4
                            if cnt % 12 == 0:
                                buffer.data[k].append(0)
                                buffer.data[k].append(0)
                                buffer.data[k].append(0)
                                buffer.data[k].append(cnt / 12)
                                buffer.writeBlockToDisk("nest_loop_join_result" + str((cnt - 1) // 12), k)
                                k = buffer.getNewBlockInBuffer()
            buffer.freeBlockInBuffer(n)
    if cnt % 12 != 0:
        buffer.writeBlockToDisk("nest_loop_join_result" + str((cnt - 1) / 12), k)
    buffer.freeBlockInBuffer(k)

def sort_merge_join(buffer):
    merge_sort_R(buffer)
    merge_sort_S(buffer)
    filename1 = "binary_selection_temp_R"
    filename2 = "binary_selection_temp2_S"
    m = int(buffer.readBlockFromDisk(filename1 + "0"))
    arr_num=6
    nlist=[]
    l=0
    for i in range(arr_num):
        n = int(buffer.readBlockFromDisk(filename2 + str(i)))
        nlist.append(n)
    k = buffer.getNewBlockInBuffer()
    cnt = 0
    f1 = 0
    f2 = 0
    i = 0
    j = 0
    before=0
    pre_f1 = f1
    pre_i=i
    pre_f2 = f2
    pre_j = j
    flag = False
    clear=False
    n=nlist[f2]
    before_a=0
    while True:
        # print(cnt//4)
        a = int(buffer.data[m][2 * i])
        b = int(buffer.data[m][2 * i + 1])
        c = int(buffer.data[n][2 * j])
        d = int(buffer.data[n][2 * j + 1])
        if a!=before_a:
            before_a=a
            pre_i=i
            pre_f1=f1
        if flag and not a==c or clear:
            # print(flag,not a==c,clear)
            # print("开始回溯","clear="+str(clear))
            # print(pre_j,pre_f2)
            if not clear:
                flag = False
                i+=1
                # print(i)
                j=pre_j
                f2=pre_f2
                n=nlist[f2]
                # print("回溯到",j,f2,n)
            else:
                clear=False
                if flag:
                    # pre_f1=f1
                    # pre_i=i
                    flag = False
                    j = pre_j
                    f2 = pre_f2
                    n = nlist[f2]
                    while True:
                        a = int(buffer.data[m][2 * i])
                        b = int(buffer.data[m][2 * i + 1])
                        c = int(buffer.data[n][2 * j])
                        d = int(buffer.data[n][2 * j + 1])
                        # print()
                        # print("clear 过程:")
                        # print("元组",a,b,c,d)
                        # print(i,j)
                        if a<c:
                            i+=1
                        elif a>c:
                            j+=1
                            # print("break")
                            break
                        else:
                            buffer.data[k].append(a)
                            buffer.data[k].append(b)
                            buffer.data[k].append(c)
                            buffer.data[k].append(d)
                            print(a,b,c,d)
                            before = a
                            flag = True
                            j += 1
                            cnt += 4
                            if cnt % 12 == 0:
                                buffer.writeBlockToDisk("sort_merge_join_result" + str((cnt - 1) // 12), k)
                                k = buffer.getNewBlockInBuffer()
                        if i==7:
                            i = 0
                            f1 += 1
                            if f1 < 16:
                                buffer.freeBlockInBuffer(m)
                                m = buffer.readBlockFromDisk(filename1 + str(f1))
                            else:
                                break
                        if j == 7:
                            j = 0
                            f2 += 1
                            if f2 < len(nlist):
                                # print("a")
                                n = nlist[f2]
                            else:
                                # print("b")
                                i+=1
                                j=pre_j
                                f2=pre_f2
                                n=nlist[f2]
                                # print("new i j",i,j)
                                if i == 7:
                                    i = 0
                                    f1 += 1
                                    if f1 < 16:
                                        buffer.freeBlockInBuffer(m)
                                        m = buffer.readBlockFromDisk(filename1 + str(f1))
                                    else:
                                        break
                clear=False
                f2=0
                pre_f2=0
                pre_j=0
                j=0
                buffer.freeBlockInBuffer(m)
                m=buffer.readBlockFromDisk(filename1+str(pre_f1))
                i=pre_i
                f1=pre_f1
                pre_f1=0
                pre_i=0
                for n in nlist:
                    buffer.freeBlockInBuffer(n)
                nlist=[]
                if l<32//arr_num+1:
                    for p in range(arr_num):
                        if l*arr_num+p<32:
                            n=int(buffer.readBlockFromDisk(filename2+str(l*arr_num+p)))
                            nlist.append(n)
                    n=nlist[f2]
                else:
                    break
                continue
        elif a < c:
            # print("a<c")
            i += 1
        elif a > c:
            # print("a>c")
            j += 1
        else:
            buffer.data[k].append(a)
            buffer.data[k].append(b)
            buffer.data[k].append(c)
            buffer.data[k].append(d)
            print(a,b,c,d)
            if not flag:
                # print("remember")
                pre_f2=f2
                pre_j=j
                # print(f2,j)
            before=a
            flag=True
            j+=1
            cnt+=4
            if cnt%12==0:
                buffer.writeBlockToDisk("sort_merge_join_result" + str((cnt - 1) // 12), k)
                k=buffer.getNewBlockInBuffer()
        if i == 7:
            i = 0
            f1 += 1
            if f1 < 16:
                buffer.freeBlockInBuffer(m)
                m = buffer.readBlockFromDisk(filename1 + str(f1))
            else:
                break
        if j == 7:
            j = 0
            f2 += 1
            if f2<len(nlist):
                n=nlist[f2]
            else:
                # print("clear  clear")
                # f2=0
                i+=1
                l+=1
                clear=True
                if i == 7:
                    i = 0
                    f1 += 1
                    if f1 < 16:
                        buffer.freeBlockInBuffer(m)
                        m = buffer.readBlockFromDisk(filename1 + str(f1))
                    else:
                        break
    if cnt % 12 != 0:
        buffer.writeBlockToDisk("sort_merge_join_result" + str((cnt - 1) // 12), k)
    for i in range(8):
        buffer.freeBlockInBuffer(i)
    filename3 = "binary_selection_temp_S"
    for i in range(16):
        ExtMem.dropBlockOnDisk(filename1 + str(i))
    for i in range(32):
        ExtMem.dropBlockOnDisk(filename2 + str(i))
        ExtMem.dropBlockOnDisk(filename3 + str(i))
    for i in range(16):
        ExtMem.dropBlockOnDisk("sort_R" + str(i))
    for i in range(32):
        ExtMem.dropBlockOnDisk("sort_S" + str(i))

def hash_join(buffer):
    dictR = {}
    dictS = {}
    filename1="r"
    filename2="s"
    hash=10
    for i in range(16):
        m=int(buffer.readBlockFromDisk(filename1+str(i)))
        for j in range(7):
            a=int(buffer.data[m][2*j])
            if a%hash in dictR.keys():
                dictR[a%hash].append((i,j))
            else:
                dictR[a%hash]=[]
                dictR[a%hash].append((i,j))
        buffer.freeBlockInBuffer(m)
    for i in range(32):
        n = int(buffer.readBlockFromDisk(filename2 + str(i)))
        for j in range(7):
            c = int(buffer.data[n][2 * j])
            # d = buffer.data[n][2 * j + 1]
            if c%hash in dictS.keys():
                dictS[c%hash].append((i, j))
            else:
                dictS[c%hash] = []
                dictS[c%hash].append((i, j))
        buffer.freeBlockInBuffer(n)
    for h in range(hash):
        if h in dictR.keys():
            dictR[h]=sorted(dictR[h])
        if h in dictS.keys():
            dictS[h]=sorted(dictS[h])
    cnt = 0
    k=buffer.getNewBlockInBuffer()
    for h in range(hash):
        for i in range(8):
            buffer.freeBlockInBuffer(i)
        if h not in dictR.keys() or h not in dictS.keys():
            continue
        listR=dictR[h]
        listS=dictS[h]
        for i,r in enumerate(listR):
            # print(i,r)
            x=r[1]
            m=buffer.readBlockFromDisk(filename1+str(r[0]))
            a=buffer.data[m][2*x]
            b=buffer.data[m][2*x+1]
            for j,s in enumerate(listS):
                y=s[1]
                n=buffer.readBlockFromDisk(filename2+str(s[0]))
                c = buffer.data[n][2 * y]
                d = buffer.data[n][2 * y + 1]
                if a==c:
                    buffer.data[k].append(a)
                    buffer.data[k].append(b)
                    buffer.data[k].append(c)
                    buffer.data[k].append(d)
                    print(a,b,c,d)
                    cnt+=4
                    if cnt%12==0:
                        buffer.writeBlockToDisk("hash_join_result" + str((cnt - 1) // 12), k)
                        k=buffer.getNewBlockInBuffer()
                buffer.freeBlockInBuffer(n)
            buffer.freeBlockInBuffer(m)
    if cnt % 12 != 0:
        buffer.writeBlockToDisk("hash_join_result" + str((cnt - 1) // 12), k)
    buffer.freeBlockInBuffer(k)


if __name__ == '__main__':
    buffer = ExtMem.Buffer(520, 64)
    # liner_selection(buffer)
    # binary_selection(buffer)
    # b_plus_tree_selection(buffer)
    # project(buffer,"R","A")
    # nest_loop_join(buffer)
    # sort_merge_join(buffer)
    # hash_join(buffer)
    # R,S=generateRS()
    # write_r_to_disk(buffer,R)
    # write_s_to_disk(buffer,S)
    # print_R_S(buffer)
    # for i in range(2):
    #     for j in range(8):
    #         n=buffer.readBlockFromDisk("sort_merge_join_result"+str(8*i+j))
    #     for x in range(8):
    #         for y in range(7):
    #             print(buffer.data[x][y*2],buffer.data[x][y*2+1])
    #     for k in range(8):
    #         buffer.freeBlockInBuffer(k)