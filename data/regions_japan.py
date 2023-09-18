
"""

    Climate regions are defined by the Japan Meteorological Agency
    https://www.data.jma.go.jp/stats/data/en/index.html

"""

REGIONS = {
    0: 'Hokkaido',
    1: 'Tohoku',
    2: 'Hokuriku',
    3: 'Kanto-Koshin',
    4: 'Kinki',
    5: 'Chugoku',
    6: 'Tokai',
    7: 'Shikoku',
    8: 'Kyushu-North',
    9: 'Kyushu-South-Amami',
    10: 'Okinawa',
}

"""
    Map locations to climate region ids
"""

LOCATIONS = {
    'Japan/Kushiro-1': 0,
    'Japan/Naze': 10,  # Officially classified as 9 -- climate is closer to 10
    'Japan/Miyakejima': 3,
    'Japan/Fukushima': 1,
    'Japan/Kagoshima': 9,
    'Japan/Saga': 8,
    'Japan/Nagasaki': 8,
    'Japan/Muroran-2': 0,
    'Japan/Tottori-2': 5,
    'Japan/Niigata': 2,
    'Japan/Toyooka': 4,
    'Japan/Nagoya-1': 6,
    'Japan/Tateyama': 2,
    'Japan/Tottori-1': 5,
    'Japan/Nago': 10,
    'Japan/Kobe': 4,
    'Japan/Tsuruga': 2,
    'Japan/Shimonoseki': 8,
    'Japan/Miyako': 1,
    'Japan/Izuhara-2': 8,
    'Japan/Shionomisaki': 4,
    'Japan/Asahikawa': 0,
    'Japan/Wakkanai': 0,
    'Japan/Fukue': 8,
    'Japan/Sendai-2': 1,
    'Japan/Mito': 3,
    'Japan/Nemuro': 0,
    'Japan/Wajima': 2,
    'Japan/Rumoi': 0,
    'Japan/Gifu': 3,
    'Japan/Hachinohe': 1,
    'Japan/Yamagata': 1,
    'Japan/Abashiri': 0,
    'Japan/Kyoto-2': 4,
    'Japan/Onahama': 1,
    'Japan/Matsuyama': 7,
    'Japan/Muroran-1': 0,
    'Japan/Oita': 8,
    'Japan/Ishigakijima': 10,
    'Japan/Esashi': 0,
    'Japan/Kushiro-2': 0,
    'Japan/Kochi-1': 7,
    'Japan/Okayama': 5,
    'Japan/Sakata': 1,
    'Japan/Fukui': 2,
    'Japan/Toyama': 2,
    'Japan/Osaka': 4,
    'Japan/Obihiro': 0,
    'Japan/Kumamoto': 8,
    'Japan/Urakawa': 0,
    'Japan/Sendai-1': 1,
    'Japan/Shizuoka': 1,
    'Japan/Minamidaitojima': 10,
    'Japan/Yakushima-2': 9,
    'Japan/Takamatsu': 7,
    'Japan/Iriomotejima': 10,
    'Japan/Kyoto-1': 4,
    'Japan/Iida': 3,
    'Japan/Nara': 4,
    'Japan/Utsunomiya': 3,
    'Japan/Hamada': 5,
    'Japan/Yokohama': 3,
    'Japan/Shinjo': 1,
    'Japan/Iwamizawa': 0,
    'Japan/Sumoto': 4,
    'Japan/Hachijojima': 3,
    # 'Japan/Hachijojima': 10,  # TODO -- remove
    'Japan/Miyakojima': 10,
    'Japan/Nagoya-2': 6,
    'Japan/Matsumoto': 3,
    'Japan/Saigo': 3,
    'Japan/Tokyo': 3,
    'Japan/Aomori': 1,
    'Japan/Hamamatsu': 6,
    'Japan/Kofu': 3,
    'Japan/Tanegashima': 9,
    # 'Japan/Tanegashima': 10,  # TODO - - remove
    'Japan/Kochi-2': 7,
    'Japan/Sapporo': 0,
    'Japan/Yakushima-1': 9,
    'Japan/Tsu': 6,
    'Japan/Kumagaya': 3,
    'Japan/Hikone': 4,
    'Japan/Fukuoka': 8,
    'Japan/Mombetsu': 0,
    'Japan/Wakayama': 4,
    'Japan/Oshima': 3,
    'Japan/Owase': 6,
    'Japan/Kanazawa': 2,
    'Japan/Maebashi': 3,
    'Japan/Nobeoka': 9,
    'Japan/Morioka': 1,
    'Japan/Shirakawa': 6,
    'Japan/Akita': 1,
    'Japan/Izuhara-1': 8,
    'Japan/Uwajima': 7,
    'Japan/Naze,Funchatoge': 10,  # Officially classified as 9 -- climate is closer to 10
    'Japan/Choshi': 3,
    'Japan/Naha': 10,
    'Japan/Matsue': 5,
    'Japan/Takada': 2,
    'Japan/Yonago': 5,
    'Japan/Takayama': 3,
    'Japan/Hiroo': 0,
    'Japan/Aikawa': 2,
    'Japan/Hakodate': 0,
    'Japan/Tokushima': 7,
    'Japan/Hiroshima': 5,
    'Japan/Kumejima': 10,
    'Japan/Yonagunijima': 10,
    'Japan/Nagano': 3,
    'Japan/Miyazaki': 9,
    'Japan/Maizuru': 4,
    'Japan/Kutchan': 0,
}

LOCATIONS_WO_OKINAWA = {k: v for k, v in LOCATIONS.items() if v != 10}
