# coding:utf-8
import random
import time
from selenium import webdriver


def start(driver):
    survey_info = get_survey_info()
    process(survey_info)


def get_survey_info():
    survey_info = {}
    page_list = driver.find_elements_by_xpath("//fieldset[contains(@id, 'fieldset')]")
    page_count = len(page_list)
    survey_info['page_count'] = len(page_list)

    this_info = {}
    for count in range(1, page_count + 1):
        div_list = driver.find_elements_by_xpath(
            f"//fieldset[contains(@id, 'fieldset{count}')]/div[contains(@class, 'div_question')]")
        this_info[count] = len(div_list)
        survey_info['page_div_count'] = this_info
    return survey_info


def process(survey_info):
    page_count = survey_info['page_count']
    page_div_count_dict = survey_info['page_div_count']
    stuid = getrandomstuid()
    print('学号:', stuid)

    # 分页处理问卷，注意第二页问卷的div标记并不是从0开始，而是从上一页最后一题的标号顺下来
    for count in range(1, page_count + 1):
        start_div = 1
        end_div = page_div_count_dict[start_div] + 1
        page_decrease = 1
        last_page = 0
        last_div = 0
        if count == 1:
            pass
        else:
            for index in range(1, count):
                start_div += page_div_count_dict[index]

            end_div = page_div_count_dict[count] + start_div + 2
        for div_count in range(start_div, end_div):
            do_ques(count, div_count, stuid)

        # 页处理完毕，点击下一页
        try:
            driver.find_element_by_id('btnNext').click()
        except:
            pass

        # 问卷填写完毕，点击提交按钮
        if count == 9:
            try:
                'submitbutton'
                driver.find_element_by_class_name('submitbutton').click()
            except:
                pass


def do_ques(count, div_count, stuid):
    textarea = ''
    atag = ''
    select = ''
    # 尝试获取textarea
    try:
        textarea = driver.find_element_by_xpath(
            f"//fieldset[contains(@id, 'fieldset{count}')]/div[contains(@id, 'div{div_count}')]")  # "//div[contains(@id,'divquestion')]"
        textarea = textarea.find_element_by_tag_name('textarea')
    except:
        textarea = False
        pass

    # 尝试获取a标签
    try:
        atag = driver.find_element_by_xpath(
            f"//fieldset[contains(@id, 'fieldset{count}')]/div[contains(@id, 'div{div_count}')]")
        atag = atag.find_element_by_tag_name('ul')
        "ul[contains(@class, 'ulradiocheck')]"
    except:
        atag = False
        pass

    # 尝试获取select下拉菜单
    try:
        select = driver.find_element_by_xpath(
            f"//fieldset[contains(@id, 'fieldset{count}')]/div[contains(@id, 'div{div_count}')]")
        select = select.find_element_by_tag_name('select')
    except:
        select = False
        pass

    # 自定义输入框内容
    if textarea != False:
        if count == 1 and div_count == 1:
            textarea.send_keys(stuid)
        if count == 9 and div_count == 301:
            textarea.send_keys(stuid)
        if count == 1 and div_count == 3:
            textarea.send_keys(getrandomname())
        if count == 1 and div_count == 4:
            textarea.send_keys('%2d' % random.randint(20, 25))

    if atag != False:
        alist = atag.find_elements_by_tag_name('a')
        # 根据选项个数 随机生成选项
        random_choice = getrandomnum(len(alist))
        alist[random_choice].click()

    if select != False:
        option_list = select.find_elements_by_tag_name('option')
        option_list.remove(option_list[0])

        radom_option = option_list[random.randint(0, len(option_list) - 1)]
        radom_option.click()


# 获取随机数
def getrandomnum(number):
    renum = random.sample(range(number), 1)
    return renum[0]


# 优化方案 模拟真实学号
def getrandomstuid():
    # stuid = ''
    # for i in range(10):
    #     stuid += random.randint(0, 9).__str__()
    # return stuid
    stuid = ''
    stuid_head_list = ["1909", "1808", "1707"]
    current_head = stuid_head_list[random.sample(range(2), 1)[0]]
    stuid += current_head
    for i in range(6):
        stuid += random.randint(0, 9).__str__()
    return stuid


# 优化方案 模拟真实姓名
def getrandomname():
    # 常用姓氏
    last_name = "赵,钱,孙,李,周,吴,郑,王,冯,陈,褚,卫,蒋,沈,韩,杨,朱,秦,尤,许,何,吕,施," \
                "张,孔,曹,严,华,金,魏,陶,姜,戚,谢,邹,喻,柏,水,窦,章,云,苏,潘,葛,奚,范," \
                "彭,郎,鲁,韦,昌,马,苗,凤,花,方,俞,任,袁,柳,酆,鲍,史,唐,费,廉,岑,薛,雷," \
                "贺,倪,汤,滕,殷,罗,毕,郝,邬,安,常,乐,于,时,傅,皮,卞,齐,康,伍,余,元,卜," \
                "顾,孟,平,黄,和,穆,萧,尹,姚,邵,湛,汪,祁,毛,禹,狄,米,贝,明,臧,计,伏,成," \
                "戴,谈,宋,茅,庞,熊,纪,舒,屈,项,祝,董,梁,杜,阮,蓝,闵,席,季,麻,强,贾,路," \
                "娄,危,江,童,颜,郭,梅,盛,林,刁,钟,徐,邱,骆,高,夏,蔡,田,樊,胡,凌,霍,虞," \
                "万,支,柯,昝,管,卢,莫,经,房,裘,缪,干,解,应,宗,丁,宣,贲,邓,郁,单,杭,洪," \
                "包,诸,左,石,崔,吉,钮,龚,程,嵇,邢,滑,裴,陆,荣,翁,荀,羊,於,惠,甄,麴,家," \
                "封,芮,羿,储,靳,汲,邴,糜,松,井,段,富,巫,乌,焦,巴,弓,牧,隗,山,谷,车,侯," \
                "宓,蓬,全,郗,班,仰,秋,仲,伊,宫,宁,仇,栾,暴,甘,钭,厉,戎,祖,武,符,刘,景," \
                "詹,束,龙,叶,幸,司,韶,郜,黎,蓟,薄,印,宿,白,怀,蒲,邰,从,鄂,索,咸,籍,赖," \
                "卓,蔺,屠,蒙,池,乔,阴,欎,胥,能,苍,双,闻,莘,党,翟,谭,贡,劳,逄,姬,申,扶," \
                "堵,冉,宰,郦,雍,舄,璩,桑,桂,濮,牛,寿,通,边,扈,燕,冀,郏,浦,尚,农,温,别," \
                "庄,晏,柴,瞿,阎,充,慕,连,茹,习,宦,艾,鱼,容,向,古,易,慎,戈,廖,庾,终,暨," \
                "居,衡,步,都,耿,满,弘,匡,国,文,寇,广,禄,阙,东,殴,殳,沃,利,蔚,越,夔,隆," \
                "师,巩,厍,聂,晁,勾,敖,融,冷,訾,辛,阚,那,简,饶,空,曾,毋,沙,乜,养,鞠,须," \
                "丰,巢,关,蒯,相,查,後,荆,红,游,竺,权,逯,盖,益,桓,公,万俟,司马,上官,欧阳," \
                "夏侯,诸葛,闻人,东方,赫连,皇甫,尉迟,公羊,澹台,公冶,宗政,濮阳,淳于,单于," \
                "太叔,申屠,公孙,仲孙,轩辕,令狐,钟离,宇文,长孙,慕容,鲜于,闾丘,司徒,司空," \
                "亓官,司寇,仉,督,子车,颛孙,端木,巫马,公西,漆雕,乐正,壤驷,公良,拓跋,夹谷," \
                "宰父,谷梁,晋,楚,闫,法,汝,鄢,涂,钦,段干,百里,东郭,南门,呼延,归,海,羊舌," \
                "微生,岳,帅,缑,亢,况,后,有,琴,梁丘,左丘,东门,西门,商,牟,佘,佴,伯,赏,南宫," \
                "墨,哈,谯,笪,年,爱,阳,佟,第五,言,福,百,家,姓,终,"
    last_name_list = last_name.split(',')

    rand2 = random.sample(range(len(last_name_list)), 2)
    rand_name = last_name_list[rand2[0]] + last_name_list[rand2[1]]
    print('姓名:', rand_name)
    return rand_name


def debug():
    stuid = getrandomstuid()
    print(stuid)


if __name__ == '__main__':
    rem_count = 1
    survey_count = 1
    driver = webdriver.Chrome()
    url = 'https://www.wjx.cn/jq/95193773.aspx'

    log_file_path = "./count.txt"
    with open(log_file_path, 'r') as file:
        rem_count = file.read()
        file.close()
    print(type(rem_count))
    if rem_count != '':
        survey_count = int(rem_count)
    while True:
        print(f'正在填写第{survey_count}份问卷')
        with open(log_file_path, 'w') as file:
            file.write(str(survey_count))
            file.close()
        driver.get(url)
        # 启动函数
        start(driver)
        # 刷新浏览器
        driver.refresh()
        # 问卷数+1
        survey_count += 1
        # 等待1秒进行下一轮
        time.sleep(1)
    # debug()
