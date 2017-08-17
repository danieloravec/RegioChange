MAX_STATION_TIME = 15  # Max minutes for train to spend in one station

STATION_CODES = {
    'Třinec centrum, nádr.': 1313142001,
    'Ostrava, Stodolní': 372825009,
    'Žilina, žel. st.': 508812004,
    'Ostrava, hl.n.': 372825008,
    'Přerov, nádr.': 2370298003,
    'Návsí (Jablunkov), nádr.': 1558071000,
    'Liptovský Mikuláš, žel. st.': 1763018002,
    'Hulín, nádr.': 2370298002,
    'Zábřeh na Moravě, nádr.': 372825004,
    'Košice, žel. st.': 1763018007,
    'Bystřice (Třinec), nádr.': 1313142002,
    'Margecany, žel. st.': 2317717000,
    'Praha, hl.n.': 372825000,
    'Čadca, žel.st.': 508812003,
    'Štrba, žel. st.': 1763018003,
    'Český Těšín, nádraží': 508812001,
    'Kysak (pri meste Prešov), žel. st.': 1763018006,
    'Olomouc, hl.n.': 372825005,
    'Poprad, Tatry': 1763018004,
    'Otrokovice, žel. st.': 2370298001,
    'Staré Město, [UH], nádraží': 2370298000,
    'Ostrava, Svinov': 372825007,
    'Hranice na M., nádr.': 372825006,
    'Vrútky, žel. st.': 1763018000,
    'Spišská Nová Ves, žel. st.': 1763018005,
    'Havířov, nádr.': 372825010,
    'Ružomberok, žel. st.': 1763018001,
    'Pardubice, hl. nádraží': 372825002,
    'Česká Třebová, nádr.': 1313142000
}

CODE_STATIONS = {
    1763018006: 'Kysak (pri meste Prešov), žel. st.',
    1763018003: 'Štrba, žel. st.',
    1763018002: 'Liptovský Mikuláš, žel. st.',
    372825000: 'Praha, hl.n.',
    372825006: 'Hranice na M., nádr.',
    508812003: 'Čadca, žel.st.',
    508812004: 'Žilina, žel. st.',
    2370298001: 'Otrokovice, žel. st.',
    372825002: 'Pardubice, hl. nádraží',
    2370298003: 'Přerov, nádr.',
    1763018004: 'Poprad, Tatry',
    372825009: 'Ostrava, Stodolní',
    1558071000: 'Návsí (Jablunkov), nádr.',
    372825004: 'Zábřeh na Moravě, nádr.',
    1313142001: 'Třinec centrum, nádr.',
    372825008: 'Ostrava, hl.n.',
    372825007: 'Ostrava, Svinov',
    1313142000: 'Česká Třebová, nádr.',
    1313142002: 'Bystřice (Třinec), nádr.',
    2370298002: 'Hulín, nádr.',
    1763018005: 'Spišská Nová Ves, žel. st.',
    372825005: 'Olomouc, hl.n.',
    1763018000: 'Vrútky, žel. st.',
    508812001: 'Český Těšín, nádraží',
    1763018001: 'Ružomberok, žel. st.',
    2370298000: 'Staré Město, [UH], nádraží',
    2317717000: 'Margecany, žel. st.',
    1763018007: 'Košice, žel. st.',
    372825010: 'Havířov, nádr.'
}

ROUTES_DICT = {
    'Praha, hl.n. Košice, žel. st.': 0,
    'Košice, žel. st. Praha, hl.n.': 1,
    'Praha, hl.n. Návsí (Jablunkov), nádr.': 2,
    'Návsí (Jablunkov), nádr. Praha, hl.n.': 3

}

ALL_ROUTES = [
    # Prague -> Kosice
    [
        372825000,
        372825002,
        1313142000,
        372825004,
        372825005,
        372825006,
        372825007,
        372825010,
        508812001,
        1313142001,
        508812003,
        508812004,
        1763018000,
        1763018001,
        1763018002,
        1763018003,
        1763018004,
        1763018005,
        1763018006,
        1763018007
    ],
    # Kosice -> Prague
    [
        1763018007,
        1763018006,
        2317717000,
        1763018005,
        1763018004,
        1763018003,
        1763018002,
        1763018001,
        1763018000,
        508812004,
        508812003,
        1313142001,
        508812001,
        372825010,
        372825008,
        372825005,
        372825004,
        372825002,
        372825000
    ],
    # Prague -> Navsi
    [
        372825000,
        372825002,
        1313142000,
        372825004,
        372825005,
        372825006,
        372825007,
        372825010,
        508812001,
        1313142001,
        1313142002,
        1558071000
    ],
    # Navsi -> Prague
    [
        1558071000,
        1313142002,
        1313142001,
        508812001,
        372825010,
        372825009,
        372825006,
        372825005,
        372825004,
        1313142000,
        372825002,
        372825000
    ]

]
