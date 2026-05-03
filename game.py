import tkinter as tk
from tkinter import ttk


class HanziFusionGame:
    BASIC_ELEMENTS = [
        "金",
        "木",
        "水",
        "火",
        "土",
        "日",
        "月",
        "人",
        "心",
        "手",
        "口",
        "廿",
        "山",
        "女",
        "竹",
        "戈",
        "十",
        "大",
        "弓",
        "刀",
        "勹",
        "牛",
        "羊",
        "羽",
        "隹",
        "雨",
        "馬",
        "骨",
        "鬼",
        "魚",
        "鳥",
        "鹿",
        "麥",
        "麻",
        "龍",
        "衣",
        "豕",
        "方",
        "臣",
        "牙",
        "耳",
    ]
    AUXILIARY_ELEMENTS = ["丨", "一", "丿", "丶", "乛", "肀", "亅", "卜", "冂", "儿", "八", "乂", "厶", "乚", "凵", "又", "乙", "幺", "丷", "阝", "辶", "力", "㐄", "立", "才", "彐", "几", "匕", "斤", "冖", "冫", "爪", "丂", "癶", "厂"]
    RADICAL_ELEMENTS = ["田", "尸", "彳", "車", "足", "言", "中", "虫", "石", "禾", "王", "門", "貝", "糸", "目", "示", "米", "宀", "巾", "走", "广"]
    STARTERS = BASIC_ELEMENTS + AUXILIARY_ELEMENTS

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("漢字合成遊戲")
        self.root.geometry("520x560")
        self.root.resizable(False, False)

        self.recipe_entries, self.recipes = self._build_recipes()
        self.unlocked = set(self.STARTERS)
        self.discovery_order = list(self.STARTERS)
        self.target_characters = self._build_target_characters()
        self.catalog_sections = self._build_catalog_sections()
        self.catalog_window: tk.Toplevel | None = None

        self.input_var = tk.StringVar()
        self.result_var = tk.StringVar(
            value="請輸入兩個到五個已解鎖的漢字，例如：音儿、甫寸、丶厂、人人土"
        )
        self.progress_var = tk.StringVar()

        self._build_ui()
        self._refresh_unlocked_display()
        self._refresh_progress()

    def _build_recipes(
        self,
    ) -> tuple[list[tuple[tuple[str, ...], str]], dict[tuple[str, ...], list[str]]]:
        raw_recipes = [
            (("土", "土"), "圭"),
            (("土", "土", "土"), "垚"),
            (("火", "火"), "炎"),
            (("火", "火"), "炏"),
            (("火", "火", "火"), "焱"),
            (("炎", "炎"), "燚"),
            (("火", "火", "火", "火"), "燚"),
            (("炎", "水"), "淡"),
            (("水", "火", "火"), "淡"),
            (("木", "木"), "林"),
            (("木", "木", "木"), "森"),
            (("木", "林"), "森"),
            (("木", "木", "火"), "焚"),
            (("林", "火"), "焚"),
            (("小", "木"), "米"),
            (("水", "水"), "沝"),
            (("水", "水", "水"), "淼"),
            (("水", "沝"), "淼"),
            (("水", "木"), "沐"),
            (("水", "古"), "沽"),
            (("水", "林"), "淋"),
            (("水", "木", "木"), "淋"),
            (("水", "圭"), "洼"),
            (("水", "土", "土"), "洼"),
            (("木", "土"), "杜"),
            (("木", "圭"), "桂"),
            (("木", "土", "土"), "桂"),
            (("火", "土"), "灶"),
            (("金", "金", "金"), "鑫"),
            (("日", "日"), "昌"),
            (("日", "日", "日"), "晶"),
            (("日", "月"), "明"),
            (("月", "月"), "朋"),
            (("日", "木"), "杲"),
            (("日", "木"), "東"),
            (("日", "木"), "杳"),
            (("人", "木"), "休"),
            (("人", "土"), "仕"),
            (("人", "火"), "伙"),
            (("人", "口"), "囚"),
            (("心", "水"), "沁"),
            (("手", "口"), "扣"),
            (("口", "木"), "杏"),
            (("口", "口", "口"), "品"),
            (("口", "昌"), "唱"),
            (("廿", "人", "木"), "茶"),
            (("廿", "明"), "萌"),
            (("廿", "早"), "草"),
            (("女", "口"), "如"),
            (("女", "古"), "姑"),
            (("山", "人"), "仙"),
            (("田", "木"), "果"),
            (("田", "心"), "思"),
            (("廿", "田"), "苗"),
            (("口", "十"), "田"),
            (("口", "十"), "古"),
            (("口", "口"), "吅"),
            (("口", "口"), "回"),
            (("田", "中"), "由"),
            (("田", "中"), "甲"),
            (("十", "一"), "干"),
            (("十", "日"), "早"),
            (("十", "亅"), "丁"),
            (("十", "丿"), "千"),
            (("十", "亅", "丶"), "寸"),
            (("十", "十", "十"), "丰"),
            (("一", "一"), "二"),
            (("一", "一", "一"), "三"),
            (("一", "土"), "王"),
            (("一", "丨", "一"), "工"),
            (("一", "口", "丷", "一"), "豆"),
            (("力", "㐄", "一", "口"), "韋"),
            (("戈", "十"), "戎"),
            (("戈", "口", "一"), "或"),
            (("弓", "丨"), "引"),
            (("竹", "由"), "笛"),
            (("竹", "夭"), "笑"),
            (("竹", "合"), "答"),
            (("竹", "巴"), "笆"),
            (("木", "火"), "杰"),
            (("木", "一"), "本"),
            (("木", "丶"), "术"),
            (("木", "古"), "枯"),
            (("木", "由"), "柚"),
            (("木", "旦"), "查"),
            (("木", "中"), "束"),
            (("木", "尌"), "樹"),
            (("木", "莫"), "模"),
            (("車", "干"), "軒"),
            (("車", "車", "車"), "轟"),
            (("月", "一"), "且"),
            (("月", "凵"), "目"),
            (("月", "干"), "肝"),
            (("月", "凵", "八"), "貝"),
            (("丰", "一", "月"), "青"),
            (("立", "日"), "音"),
            (("乛", "木"), "子"),
            (("卜", "口"), "占"),
            (("一", "丿", "口"), "石"),
            (("丿", "木"), "禾"),
            (("田", "丨"), "由"),
            (("日", "一"), "旦"),
            (("日", "一", "卜", "人"), "是"),
            (("日", "丿"), "白"),
            (("女", "由"), "妯"),
            (("女", "旦"), "妲"),
            (("大", "一"), "天"),
            (("大", "丿"), "夭"),
            (("大", "丶"), "太"),
            (("大", "丶"), "犬"),
            (("戈", "丶"), "戍"),
            (("丶", "冖"), "宀"),
            (("丶", "十", "水"), "求"),
            (("口", "丿"), "尸"),
            (("丿", "人"), "彳"),
            (("乛", "亅"), "了"),
            (("丨", "冂"), "巾"),
            (("口", "丨"), "中"),
            (("口", "丨", "丨"), "罒"),
            (("口", "口", "丿"), "呂"),
            (("口", "八"), "四"),
            (("口", "土"), "吉"),
            (("卜", "口", "了"), "亨"),
            (("卜", "几"), "亢"),
            (("女", "子"), "好"),
            (("木", "子"), "李"),
            (("人", "子"), "仔"),
            (("人", "圭"), "佳"),
            (("人", "千"), "仟"),
            (("人", "八", "口"), "谷"),
            (("人", "㐄"), "年"),
            (("人", "一", "口"), "合"),
            (("人", "人"), "从"),
            (("人", "人", "土"), "坐"),
            (("人", "共"), "供"),
            (("人", "一", "乛"), "今"),
            (("人", "一", "乛", "丶"), "令"),
            (("人", "一", "吅", "从"), "僉"),
            (("女", "且"), "姐"),
            (("人", "旦"), "但"),
            (("二", "儿"), "元"),
            (("二", "厶"), "云"),
            (("二", "小"), "示"),
            (("二", "亅"), "亍"),
            (("几", "丶"), "凡"),
            (("勹", "冫"), "勻"),
            (("小", "月"), "肖"),
            (("月", "土"), "肚"),
            (("月", "旦"), "胆"),
            (("月", "由"), "胄"),
            (("月", "田"), "胃"),
            (("月", "巴"), "肥"),
            (("丶", "王"), "玉"),
            (("丶", "十", "月"), "甫"),
            (("肀", "水"), "隶"),
            (("水", "由"), "油"),
            (("水", "囚"), "泅"),
            (("水", "且"), "沮"),
            (("水", "胡"), "湖"),
            (("水", "聿"), "津"),
            (("水", "干"), "汗"),
            (("水", "共"), "洪"),
            (("水", "喿"), "澡"),
            (("水", "彎"), "灣"),
            (("水", "工"), "江"),
            (("水", "孱"), "潺"),
            (("水", "絜"), "潔"),
            (("水", "肖"), "消"),
            (("水", "朝"), "潮"),
            (("尸", "水"), "尿"),
            (("手", "苗"), "描"),
            (("手", "由"), "抽"),
            (("手", "戈"), "找"),
            (("手", "疌"), "捷"),
            (("手", "喿"), "操"),
            (("找", "丿"), "我"),
            (("心", "旦"), "怛"),
            (("中", "心"), "忠"),
            (("心", "丿", "丶"), "必"),
            (("心", "昔"), "惜"),
            (("廿", "古"), "苦"),
            (("廿", "一", "八"), "共"),
            (("廿", "一", "日"), "昔"),
            (("人", "古"), "估"),
            (("月", "古"), "胡"),
            (("木", "戔"), "棧"),
            (("山", "山"), "出"),
            (("山", "由"), "岫"),
            (("竹", "本"), "笨"),
            (("竹", "聿"), "筆"),
            (("禾", "火"), "秋"),
            (("禾", "子"), "季"),
            (("禾", "日"), "香"),
            (("禾", "口"), "和"),
            (("禾", "厶"), "私"),
            (("禾", "且"), "租"),
            (("禾", "白"), "粕"),
            (("臣", "又"), "臤"),
            (("千", "口"), "舌"),
            (("尸", "古"), "居"),
            (("尸", "子", "子", "子"), "孱"),
            (("彳", "亍"), "行"),
            (("彳", "聿"), "律"),
            (("十", "田", "十"), "車"),
            (("廿", "中", "十"), "革"),
            (("廿", "隹"), "雈"),
            (("廿", "隹"), "萑"),
            (("十", "聿", "女"), "妻"),
            (("肀", "廿"), "聿"),
            (("肀", "土", "日"), "書"),
            (("肀", "土", "田", "一"), "畫"),
            (("肀", "土", "日", "一"), "晝"),
            (("車", "由"), "軸"),
            (("車", "甫"), "輔"),
            (("卜", "口", "人"), "足"),
            (("土", "卜", "人"), "走"),
            (("卜", "一", "一", "口"), "言"),
            (("言", "十"), "計"),
            (("言", "丁"), "訂"),
            (("言", "古"), "詁"),
            (("言", "青"), "請"),
            (("言", "寺"), "詩"),
            (("言", "羊"), "詳"),
            (("言", "隹"), "誰"),
            (("示", "羊"), "祥"),
            (("示", "見"), "視"),
            (("示", "且"), "祖"),
            (("言", "舌"), "話"),
            (("言", "戠"), "識"),
            (("言", "登"), "證"),
            (("糸", "隹"), "維"),
            (("中", "中"), "串"),
            (("吅", "田", "十"), "單"),
            (("口", "口", "田", "十"), "單"),
            (("吅", "頁", "吅"), "囂"),
            (("吅", "犬", "吅"), "器"),
            (("中", "一", "丶"), "虫"),
            (("虫", "由"), "蚰"),
            (("虫", "古"), "蛄"),
            (("虫", "引"), "蚓"),
            (("虫", "圭"), "蛙"),
            (("虫", "且"), "蛆"),
            (("日", "丨", "日", "亅"), "門"),
            (("雨", "田", "乚"), "電"),
            (("雨", "田"), "雷"),
            (("雨", "云"), "雲"),
            (("雨", "林"), "霖"),
            (("雨", "相"), "霜"),
            (("雨", "彐"), "雪"),
            (("雨", "肖"), "霄"),
            (("雨", "革", "月"), "霸"),
            (("女", "畫"), "嫿"),
            (("女", "圭"), "娃"),
            (("女", "未"), "妹"),
            (("幺", "小"), "糸"),
            (("幺", "小"), "糹"),
            (("十", "木"), "未"),
            (("十", "木"), "末"),
            (("人", "十"), "午"),
            (("人", "十"), "什"),
            (("人", "乂"), "攵"),
            (("人", "丨", "攵"), "攸"),
            (("人", "攸"), "修"),
            (("人", "隹"), "倠"),
            (("羊", "大"), "美"),
            (("羊", "我"), "義"),
            (("羊", "儿"), "羌"),
            (("丿", "土"), "壬"),
            (("一", "一", "亅"), "亍"),
            (("一", "丁"), "亍"),
            (("吉", "丷", "一", "寸"), "尌"),
            (("廿", "一"), "甘"),
            (("廿", "一", "田", "八"), "黃"),
            (("廿", "日", "大"), "莫"),
            (("廿", "田", "禸"), "萬"),
            (("廿", "魚", "禾"), "蘇"),
            (("卜", "允"), "充"),
            (("卜", "乂"), "文"),
            (("糸", "充"), "統"),
            (("糸", "言", "糸", "木"), "欒"),
            (("糸", "言", "糸", "弓"), "彎"),
            (("丿", "口", "廿"), "囪"),
            (("丿", "又", "冫"), "冬"),
            (("丿", "又"), "夂"),
            (("囪", "心"), "悤"),
            (("糸", "悤"), "總"),
            (("束", "刀", "貝"), "賴"),
            (("彳", "十", "罒", "一", "心"), "德"),
            (("卜", "口", "子"), "享"),
            (("勹", "丿", "丿"), "勿"),
            (("勿", "丶"), "匆"),
            (("木", "日", "一", "勿"), "楊"),
            (("日", "勿"), "易"),
            (("足", "易"), "踢"),
            (("厶", "儿"), "允"),
            (("享", "阝"), "郭"),
            (("口", "乚"), "巳"),
            (("一", "乚"), "七"),
            (("卜", "八"), "六"),
            (("十", "乚"), "九"),
            (("一", "丿", "日"), "百"),
            (("亅", "八"), "小"),
            (("牛", "勿"), "物"),
            (("尚", "貝"), "賞"),
            (("一", "力", "一"), "五"),
            (("五", "口"), "吾"),
            (("言", "吾"), "語"),
            (("王", "元"), "玩"),
            (("貝", "刀"), "則"),
            (("卜", "日", "十"), "卓"),
            (("卜", "日", "木"), "桌"),
            (("目", "儿"), "見"),
            (("目", "木"), "相"),
            (("目", "青"), "睛"),
            (("目", "米"), "眯"),
            (("目", "八"), "貝"),
            (("丿", "米"), "釆"),
            (("丿", "小", "木"), "采"),
            (("一", "丿", "貝"), "頁"),
            (("廿", "采"), "菜"),
            (("田", "土"), "里"),
            (("米", "青"), "精"),
            (("禾", "刀"), "利"),
            (("禾", "責"), "積"),
            (("禾", "呈"), "程"),
            (("車", "九"), "軌"),
            (("辶", "由"), "迪"),
            (("辶", "豆"), "逗"),
            (("辶", "白"), "迫"),
            (("辶", "周"), "週"),
            (("行", "圭"), "街"),
            (("勹", "巳"), "包"),
            (("足", "包"), "跑"),
            (("甘", "木"), "柑"),
            (("白", "羽"), "習"),
            (("白", "王"), "皇"),
            (("衣", "由"), "袖"),
            (("衣", "包"), "袍"),
            (("衣", "尚"), "裳"),
            (("門", "日"), "間"),
            (("門", "口"), "問"),
            (("門", "人"), "閃"),
            (("魚", "羊"), "鮮"),
            (("魚", "里"), "鯉"),
            (("水", "魚"), "漁"),
            (("魚", "焦"), "鮫"),
            (("馬", "又"), "馭"),
            (("麻", "鬼"), "魔"),
            (("冂", "一", "口"), "同"),
            (("土", "寸"), "寺"),
            (("米", "且"), "粗"),
            (("禾", "鬼"), "魏"),
            (("糸", "田"), "累"),
            (("糸", "責"), "績"),
            (("白", "鬼"), "魄"),
            (("鬼", "云"), "魂"),
            (("頁", "豆"), "頭"),
            (("音", "心"), "意"),
            (("音", "十"), "章"),
            (("音", "戈"), "戠"),
            (("音", "儿"), "竟"),
            (("中", "一", "貝"), "貴"),
            (("辶", "韋"), "違"),
            (("口", "韋"), "圍"),
            (("貝", "才"), "財"),
            (("八", "厶"), "公"),
            (("八", "乂"), "父"),
            (("公", "頁"), "頌"),
            (("門", "馬"), "闖"),
            (("卜", "貝"), "貞"),
            (("示", "貞"), "禎"),
            (("彐", "工", "口", "寸"), "尋"),
            (("立", "木"), "亲"),
            (("立", "羽"), "翌"),
            (("立", "羽"), "翊"),
            (("亲", "見"), "親"),
            (("亲", "斤"), "新"),
            (("辶", "貴"), "遺"),
            (("女", "霜"), "孀"),
            (("女", "家"), "嫁"),
            (("門", "才"), "閉"),
            (("公", "心"), "忪"),
            (("公", "羽"), "翁"),
            (("幺", "幺", "白", "木"), "樂"),
            (("王", "王"), "玨"),
            (("王", "玉"), "珏"),
            (("玨", "文"), "斑"),
            (("玨", "丶", "丿"), "班"),
            (("玨", "今"), "琴"),
            (("玨", "必"), "瑟"),
            (("玨", "比"), "琵"),
            (("玨", "巴"), "琶"),
            (("莫", "土"), "墓"),
            (("莫", "心"), "慕"),
            (("日", "莫"), "暮"),
            (("日", "青"), "晴"),
            (("水", "莫"), "漠"),
            (("水", "青"), "清"),
            (("月", "犬"), "肰"),
            (("手", "合"), "拿"),
            (("人", "言"), "信"),
            (("女", "馬"), "媽"),
            (("口", "馬"), "嗎"),
            (("口", "今"), "吟"),
            (("口", "令"), "命"),
            (("口", "合"), "哈"),
            (("今", "丶"), "令"),
            (("今", "心"), "念"),
            (("日", "乚"), "巴"),
            (("日", "肰"), "猒"),
            (("田", "力"), "男"),
            (("王", "令"), "玲"),
            (("雨", "令"), "零"),
            (("金", "同"), "銅"),
            (("金", "帛"), "錦"),
            (("金", "戔"), "錢"),
            (("乂", "乂"), "爻"),
            (("大", "爻", "爻"), "爽"),
            (("大", "隹"), "奞"),
            (("奞", "寸"), "奪"),
            (("奞", "田"), "奮"),
            (("匕", "匕"), "比"),
            (("父", "巴"), "爸"),
            (("父", "斤"), "斧"),
            (("甫", "寸"), "尃"),
            (("丰", "丰", "彐", "心"), "慧"),
            (("厶", "冂"), "禸"),
            (("冂", "土"), "冉"),
            (("冫", "馬"), "馮"),
            (("土", "勻"), "均"),
            (("土", "儿", "夂"), "夌"),
            (("凡", "虫"), "風"),
            (("凡", "鳥"), "鳳"),
            (("几", "皇"), "凰"),
            (("几", "水"), "殳"),
            (("林", "凡"), "梵"),
            (("林", "鹿"), "麓"),
            (("林", "示"), "禁"),
            (("木", "示"), "柰"),
            (("攸", "木"), "條"),
            (("臤", "貝"), "賢"),
            (("臤", "土"), "堅"),
            (("臤", "豆"), "豎"),
            (("臣", "人"), "臥"),
            (("牙", "隹"), "雅"),
            (("由", "丂"), "甹"),
            (("品", "木"), "喿"),
            (("求", "衣"), "裘"),
            (("巾", "白"), "帛"),
            (("口", "月"), "肙"),
            (("口", "貝"), "員"),
            (("口", "耳"), "咠"),
            (("圭", "寸"), "封"),
            (("封", "帛"), "幫"),
            (("卜", "回", "日", "一"), "亶"),
            (("十", "尃"), "博"),
            (("丰", "一", "貝"), "責"),
            (("丰", "刀", "糸"), "絜"),
            (("山", "丰", "丰", "豆"), "豐"),
            (("山", "幺", "幺"), "幽"),
            (("十", "日", "十", "人"), "倝"),
            (("十", "肀", "卜", "人"), "疌"),
            (("戈", "戈"), "戔"),
            (("倝", "干"), "幹"),
            (("倝", "羽"), "翰"),
            (("十", "日", "十", "月"), "朝"),
            (("厶", "儿", "夂"), "夋"),
            (("冂", "土", "口"), "周"),
            (("小", "冖", "口"), "尚"),
            (("尚", "匕", "日"), "嘗"),
            (("口", "嘗"), "嚐"),
            (("罒", "維"), "羅"),
            (("口", "羅"), "囉"),
            (("匕", "頁"), "頃"),
            (("頃", "禾"), "穎"),
            (("魚", "日"), "魯"),
            (("廿", "中", "夫", "隹"), "難"),
            (("隹", "火"), "焦"),
            (("廿", "焦"), "蕉"),
            (("炏", "冖", "木"), "榮"),
            (("炏", "冖", "虫"), "螢"),
            (("炏", "冖", "呂"), "營"),
            (("走", "肖"), "趙"),
            (("維", "巾"), "帷"),
            (("宀", "女"), "安"),
            (("宀", "子"), "字"),
            (("宀", "元"), "完"),
            (("宀", "豕"), "家"),
            (("宀", "必"), "宓"),
            (("宀", "示"), "宗"),
            (("宓", "山"), "密"),
            (("木", "帛"), "棉"),
            (("木", "安"), "案"),
            (("木", "東"), "棟"),
            (("白", "放"), "敫"),
            (("工", "力"), "功"),
            (("工", "丂"), "巧"),
            (("工", "頁"), "項"),
            (("方", "攵"), "放"),
            (("方", "人"), "仿"),
            (("言", "方"), "訪"),
            (("木", "方"), "枋"),
            (("心", "青"), "情"),
            (("虫", "青"), "蜻"),
            (("尚", "巾"), "常"),
            (("令", "頁"), "領"),
            (("口", "壬"), "呈"),
            (("口", "員"), "圓"),
            (("臥", "品"), "臨"),
            (("柰", "隶"), "隸"),
            (("糸", "敫"), "繳"),
            (("萑", "吅"), "雚"),
            (("雚", "見"), "觀"),
            (("立", "里"), "童"),
            (("丨", "丨", "丨"), "川"),
            (("川", "丶", "丶", "丶"), "州"),
            (("水", "州"), "洲"),
            (("癶", "殳"), "癹"),
            (("癹", "弓"), "發"),
            (("癶", "豆"), "登"),
            (("癶", "天"), "癸"),
            (("夭", "口", "冂", "口"), "喬"),
            (("卜", "口", "冂", "口"), "高"),
            (("火", "頁"), "煩"),
            (("丶", "厂"), "广"),
            (("厂", "猒"), "厭"),
            (("厭", "土"), "壓"),
            (("广", "倠", "心"), "應"),
            (("又", "又", "又", "又"), "叕"),
            (("耳", "又"), "取"),
            (("耳", "門"), "聞"),
            (("女", "取"), "娶"),
            (("走", "取"), "趣"),
            (("車", "咠"), "輯"),
            (("广", "黃"), "廣"),
            (("木", "高"), "槁"),
            (("木", "焦"), "樵"),
            (("水", "登"), "澄"),
            (("耳", "東"), "陳"),
            (("广", "坐"), "座"),
            (("人", "十", "山"), "缶"),
            (("辶", "月", "缶"), "遙"),
            (("難", "鳥"), "歡"),
            (("觀", "門"), "關"),
            (("博", "手"), "搏"),
            (("攸", "心"), "悠"),
            (("攸", "火"), "倏"),
            (("焦", "心"), "憔"),
            (("登", "手"), "撜"),
        ]

        recipes: dict[tuple[str, ...], list[str]] = {}
        for ingredients, result in raw_recipes:
            normalized = self._normalize_chars(*ingredients)
            recipes.setdefault(normalized, []).append(result)

        return raw_recipes, recipes

    def _build_target_characters(self) -> set[str]:
        targets = set(self.STARTERS)
        targets.update(self.RADICAL_ELEMENTS)
        targets.update(result for _, result in self.recipe_entries)
        return targets

    def _build_catalog_sections(self) -> list[tuple[str, list[str]]]:
        signatures = self._build_character_signatures()
        categories: dict[int, list[str]] = {}
        two_element_sections: dict[str, list[str]] = {
            "基本元素 + 輔助元素": [],
            "基本元素 + 基本元素": [],
            "使用 2 個不同元素": [],
        }

        ordered_results: list[str] = []
        for _, result in self.recipe_entries:
            if result not in ordered_results:
                ordered_results.append(result)

        for character in ordered_results:
            signature = signatures.get(character)
            if signature is None:
                continue

            distinct_count = len(signature)
            if distinct_count == 2:
                basic_count = sum(1 for item in signature if item in self.BASIC_ELEMENTS)
                auxiliary_count = sum(
                    1 for item in signature if item in self.AUXILIARY_ELEMENTS
                )
                if basic_count == 1 and auxiliary_count == 1:
                    two_element_sections["基本元素 + 輔助元素"].append(character)
                elif basic_count == 2:
                    two_element_sections["基本元素 + 基本元素"].append(character)
                else:
                    two_element_sections["使用 2 個不同元素"].append(character)
            else:
                categories.setdefault(distinct_count, []).append(character)

        sections: list[tuple[str, list[str]]] = [
            ("基本元素", list(self.BASIC_ELEMENTS)),
            ("輔助元素", list(self.AUXILIARY_ELEMENTS)),
            ("部首元素", list(self.RADICAL_ELEMENTS)),
        ]
        if 1 in categories:
            sections.append(("使用 1 個不同元素", categories.pop(1)))

        sections.append(("基本元素 + 輔助元素", two_element_sections["基本元素 + 輔助元素"]))
        sections.append(("基本元素 + 基本元素", two_element_sections["基本元素 + 基本元素"]))
        sections.append(("使用 2 個不同元素", two_element_sections["使用 2 個不同元素"]))

        for count in sorted(categories.keys()):
            sections.append((f"使用 {count} 個不同元素", categories[count]))
        return sections

    def _build_character_signatures(self) -> dict[str, frozenset[str]]:
        signatures: dict[str, frozenset[str]] = {
            starter: frozenset({starter}) for starter in self.STARTERS
        }
        changed = True
        while changed:
            changed = False
            for ingredients, result in self.recipe_entries:
                ingredient_signatures = []
                for ingredient in ingredients:
                    signature = signatures.get(ingredient)
                    if signature is None:
                        ingredient_signatures = []
                        break
                    ingredient_signatures.append(signature)

                if not ingredient_signatures:
                    continue

                merged_signature = frozenset().union(*ingredient_signatures)
                current_signature = signatures.get(result)
                if (
                    current_signature is None
                    or len(merged_signature) < len(current_signature)
                ):
                    signatures[result] = merged_signature
                    changed = True

        return signatures

    def _build_ui(self) -> None:
        self.root.configure(bg="#f6efe3")

        title = tk.Label(
            self.root,
            text="漢字合成遊戲",
            font=("Microsoft JhengHei UI", 24, "bold"),
            bg="#f6efe3",
            fg="#5f4630",
        )
        title.pack(pady=(18, 8))

        subtitle = tk.Label(
            self.root,
            text="從金木水火土日月人心手口廿山女竹戈十大弓刀勹牛羊羽隹雨馬骨鬼魚鳥鹿麥麻龍衣豕方臣牙耳出發，輔助元素有丨一丿丶乛肀亅卜冂儿八乂厶乚凵又乙幺丷阝辶力㐄立才彐几匕斤冖冫爪丂癶厂，部首元素有田尸彳車足言中虫石禾王門貝糸目示米宀巾走广",
            font=("Microsoft JhengHei UI", 11),
            bg="#f6efe3",
            fg="#7a6854",
        )
        subtitle.pack(pady=(0, 14))

        input_frame = tk.LabelFrame(
            self.root,
            text="開始合成",
            font=("Microsoft JhengHei UI", 11, "bold"),
            bg="#fffaf1",
            fg="#5f4630",
            padx=12,
            pady=12,
        )
        input_frame.pack(fill="x", padx=20, pady=(8, 12))

        instruction = tk.Label(
            input_frame,
            text="輸入兩個到五個字，例如：音儿、甫寸、丶厂、人人土",
            font=("Microsoft JhengHei UI", 11),
            bg="#fffaf1",
            fg="#6f5c47",
        )
        instruction.pack(anchor="w", pady=(0, 10))

        entry = ttk.Entry(
            input_frame,
            textvariable=self.input_var,
            font=("Microsoft JhengHei UI", 16),
            justify="center",
        )
        entry.pack(fill="x", ipady=8)
        entry.focus()
        entry.bind("<Return>", self._handle_enter)

        button_row = tk.Frame(input_frame, bg="#fffaf1")
        button_row.pack(fill="x", pady=(12, 0))

        craft_button = ttk.Button(button_row, text="合成", command=self.craft)
        craft_button.pack(side="left")

        reset_button = ttk.Button(button_row, text="清空輸入", command=self.clear_input)
        reset_button.pack(side="left", padx=(10, 0))

        catalog_button = ttk.Button(button_row, text="圖鑑", command=self.open_catalog)
        catalog_button.pack(side="left", padx=(10, 0))

        result_frame = tk.LabelFrame(
            self.root,
            text="結果",
            font=("Microsoft JhengHei UI", 11, "bold"),
            bg="#fffaf1",
            fg="#5f4630",
            padx=12,
            pady=12,
        )
        result_frame.pack(fill="x", padx=20, pady=(0, 12))

        result_label = tk.Label(
            result_frame,
            textvariable=self.result_var,
            font=("Microsoft JhengHei UI", 12),
            bg="#fffaf1",
            fg="#2f241a",
            justify="left",
            anchor="w",
            wraplength=450,
        )
        result_label.pack(fill="x")

        progress_frame = tk.LabelFrame(
            self.root,
            text="收集進度",
            font=("Microsoft JhengHei UI", 11, "bold"),
            bg="#fffaf1",
            fg="#5f4630",
            padx=12,
            pady=12,
        )
        progress_frame.pack(fill="x", padx=20)

        progress_label = tk.Label(
            progress_frame,
            textvariable=self.progress_var,
            font=("Microsoft JhengHei UI", 13, "bold"),
            bg="#fffaf1",
            fg="#2f241a",
        )
        progress_label.pack(anchor="w")

    def _handle_enter(self, _event: tk.Event) -> None:
        self.craft()

    def _normalize_chars(self, *chars: str) -> tuple[str, ...]:
        return tuple(sorted(chars))

    def _refresh_unlocked_display(self) -> None:
        self._refresh_catalog_display()

    def _refresh_catalog_display(self) -> None:
        if self.catalog_window is None or not self.catalog_window.winfo_exists():
            return

        for character, label in self.catalog_labels.items():
            if character in self.unlocked:
                label.config(bg="#d8f0d2", fg="#2f6b2f")
            else:
                label.config(bg="#e7dfd4", fg="#8f8578")

    def open_catalog(self) -> None:
        if self.catalog_window is not None and self.catalog_window.winfo_exists():
            self.catalog_window.lift()
            self.catalog_window.focus_force()
            self._refresh_catalog_display()
            return

        self.catalog_window = tk.Toplevel(self.root)
        self.catalog_window.title("漢字圖鑑")
        self.catalog_window.geometry("520x560")
        self.catalog_window.resizable(False, False)
        self.catalog_window.configure(bg="#f6efe3")
        self.catalog_window.protocol("WM_DELETE_WINDOW", self._close_catalog)

        title = tk.Label(
            self.catalog_window,
            text="漢字圖鑑",
            font=("Microsoft JhengHei UI", 20, "bold"),
            bg="#f6efe3",
            fg="#5f4630",
        )
        title.pack(pady=(16, 8))

        legend = tk.Label(
            self.catalog_window,
            text="綠色是已擁有，灰色是未知。",
            font=("Microsoft JhengHei UI", 10),
            bg="#f6efe3",
            fg="#6f5c47",
        )
        legend.pack()

        catalog_frame = tk.Frame(self.catalog_window, bg="#fffaf1")
        catalog_frame.pack(fill="both", expand=True, padx=20, pady=(12, 20))

        self.catalog_canvas = tk.Canvas(
            catalog_frame,
            bg="#fffaf1",
            highlightthickness=0,
            bd=0,
        )
        scrollbar = ttk.Scrollbar(
            catalog_frame,
            orient="vertical",
            command=self.catalog_canvas.yview,
        )
        self.catalog_canvas.configure(yscrollcommand=scrollbar.set)

        self.catalog_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.catalog_grid = tk.Frame(self.catalog_canvas, bg="#fffaf1", padx=12, pady=12)
        self.catalog_canvas_window = self.catalog_canvas.create_window(
            (0, 0),
            window=self.catalog_grid,
            anchor="nw",
        )
        self.catalog_grid.bind("<Configure>", self._on_catalog_frame_configure)
        self.catalog_canvas.bind("<Configure>", self._on_catalog_canvas_configure)
        self.catalog_canvas.bind("<Enter>", self._bind_catalog_mousewheel)
        self.catalog_canvas.bind("<Leave>", self._unbind_catalog_mousewheel)

        self.catalog_labels: dict[str, tk.Label] = {}
        columns = 6
        row_index = 0
        for title_text, characters in self.catalog_sections:
            section_title = tk.Label(
                self.catalog_grid,
                text=title_text,
                font=("Microsoft JhengHei UI", 13, "bold"),
                bg="#fffaf1",
                fg="#5f4630",
                anchor="w",
            )
            section_title.grid(
                row=row_index,
                column=0,
                columnspan=columns,
                sticky="w",
                pady=(4, 8),
            )
            row_index += 1

            for index, character in enumerate(characters):
                row = row_index + (index // columns)
                column = index % columns
                label = tk.Label(
                    self.catalog_grid,
                    text=character,
                    font=("Microsoft JhengHei UI", 22, "bold"),
                    width=3,
                    height=1,
                    relief="ridge",
                    bd=1,
                )
                label.grid(row=row, column=column, padx=6, pady=6, sticky="nsew")
                label.bind(
                    "<Button-1>",
                    lambda _event, value=character: self._pick_catalog_character(value),
                )
                self.catalog_labels[character] = label

            row_index += (len(characters) + columns - 1) // columns

        for column in range(columns):
            self.catalog_grid.grid_columnconfigure(column, weight=1)

        self._refresh_catalog_display()

    def _close_catalog(self) -> None:
        if self.catalog_window is not None and self.catalog_window.winfo_exists():
            self._unbind_catalog_mousewheel()
            self.catalog_window.destroy()
        self.catalog_window = None

    def _on_catalog_frame_configure(self, _event: tk.Event) -> None:
        self.catalog_canvas.configure(scrollregion=self.catalog_canvas.bbox("all"))

    def _on_catalog_canvas_configure(self, event: tk.Event) -> None:
        self.catalog_canvas.itemconfigure(self.catalog_canvas_window, width=event.width)

    def _on_catalog_mousewheel(self, event: tk.Event) -> None:
        self.catalog_canvas.yview_scroll(int(-event.delta / 120), "units")

    def _bind_catalog_mousewheel(self, _event: tk.Event) -> None:
        if self.catalog_window is not None and self.catalog_window.winfo_exists():
            self.catalog_window.bind_all("<MouseWheel>", self._on_catalog_mousewheel)

    def _unbind_catalog_mousewheel(self, _event: tk.Event | None = None) -> None:
        if self.catalog_window is not None and self.catalog_window.winfo_exists():
            self.catalog_window.unbind_all("<MouseWheel>")

    def _refresh_progress(self) -> None:
        unlocked_count = len(self.unlocked.intersection(self.target_characters))
        total_count = len(self.target_characters)
        self.progress_var.set(f"已收集 {unlocked_count} / {total_count}")

    def _pick_catalog_character(self, character: str) -> None:
        if character not in self.unlocked:
            self.result_var.set(f"{character} 還沒解鎖，現在不能加入輸入欄。")
            return

        current_text = "".join(self.input_var.get().split())
        if len(current_text) >= 5:
            self.result_var.set("輸入欄最多只能放五個字，請先清空或合成一次。")
            return

        self.input_var.set(current_text + character)
        self.root.focus_force()

    def clear_input(self) -> None:
        self.input_var.set("")

    def craft(self) -> None:
        raw_text = self.input_var.get()
        text = "".join(raw_text.split())

        if len(text) not in (2, 3, 4, 5):
            self.result_var.set("請輸入兩個、三個、四個或五個漢字，例如：音儿、甫寸、丶厂、人人土。")
            return

        chars = list(text)

        missing = [char for char in chars if char not in self.unlocked]
        if missing:
            self.result_var.set(f"不能使用未解鎖的字：{'、'.join(missing)}")
            return

        results = self.recipes.get(self._normalize_chars(*chars))

        recipe_text = " + ".join(chars)
        if results is None:
            self.result_var.set(f"{recipe_text} 沒有產生新字，這個配方目前無法合成。")
            return

        recipe_results = list(dict.fromkeys(results))
        new_results = [result for result in recipe_results if result not in self.unlocked]
        recipe_result_text = "、".join(recipe_results)

        if not new_results:
            self.result_var.set(f"{recipe_text} = {recipe_result_text}，這些字都已經解鎖過了。")
            return

        for result in new_results:
            self.unlocked.add(result)
            self.discovery_order.append(result)
        self._refresh_unlocked_display()
        self._refresh_progress()

        if self._has_completed_collection():
            self.result_var.set(
                f"{recipe_text} = {recipe_result_text}。恭喜你收集完成，所有可合成漢字都已解鎖。"
            )
        elif len(new_results) == len(recipe_results):
            self.result_var.set(f"{recipe_text} = {recipe_result_text}。成功解鎖新字！")
        else:
            self.result_var.set(
                f"{recipe_text} = {recipe_result_text}。新解鎖：{'、'.join(new_results)}。"
            )

        self.clear_input()

    def _has_completed_collection(self) -> bool:
        return self.target_characters.issubset(self.unlocked)


def main() -> None:
    root = tk.Tk()
    HanziFusionGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
