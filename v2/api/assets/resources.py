core_resources = {

    # basic resources
    '_question_marks': {
        'type': 'basic_resources',
        'name': '???',
        'keywords': ['organ', 'hide', 'bone','consumable'],
        'desc': 'You have no idea what monster bit this is. Can be used as a bone, organ, or hide!',
    },
    'broken_lantern': {
        'type': 'basic_resources',
        'name': 'Broken Lantern',
        'keywords': ['scrap'],
        'desc': '<i>Remains of an extinguished lantern.</i>',
    },
    'love_juice': {
       'type': 'basic_resources',
       'name': 'Love Juice',
       'keywords': ['organ','consumable']
    },
    'monster_bone': {
        'type': 'basic_resources',
        'name': 'Monster Bone',
        'keywords': ['bone']
    },
    'monster_hide': {
        'type': 'basic_resources',
        'name': 'Monster Hide',
        'keywords': ['hide'],
        'desc': '<i>The skin of a beast.</i>',
    },
    'monster_organ': {
        'type': 'basic_resources',
        'name': 'Monster Organ',
        'keywords': ['organ']
    },
    'scrap': {
        'type': 'basic_resources',
        'name': 'Scrap',
        'keywords': ['scrap']
    },
    'skull': {
        'type': 'basic_resources',
        'name': 'Skull',
        'keywords': ['bone'],
        'desc': 'When you gain this, a survivor of your choice gains +1 insanity.',
    },

    # strange resources
    'black_lichen': {
        'desc': 'Malleable, pungent and attractive.<br/>You may <b>consume</b> this. If you do, your lips turn grey, your hair whitens, and you become infertile. Gain +1 courage, +1 understanding and suffer the <b>destroyed genitals</b> severe waist injury.',
        'keywords': ['bone','organ','hide','consumable','other'],
        'type': 'strange_resources',
        'name': 'Black Lichen',
    },
    'cocoon_membrane': {
        'desc': 'Thin copper hairs permeate this jellylike substance.<br/>Lanterns are repelled by the copper hairs, their light bending to avoid them.',
        'keywords': ['organ', 'other'],
        'type': 'strange_resources',
        'name': 'Cocoon Membrane',
    },
    'elder_cat_teeth': {
        'type': 'strange_resources',
        'name': 'Elder Cat Teeth',
        'keywords': ['bone'],
        'desc': 'As sharp as they are strange.',
    },
    'fresh_acanthus': {
        'type': 'strange_resources',
        'name': 'Fresh Acanthus',
        'keywords': ['herb'],
        'desc': 'Archive this to fully heal 1 hit location, including injury levels and armor points.',
    },
    'iron': {
        'type': 'strange_resources',
        'name': 'Iron',
        'keywords': ['scrap'],
        'desc': 'Harder than bone.',
    },
    'lantern_tube': {
        'desc': "A fleshy, muscle-lined tube.<br/>When you gain this, roll 1d10. On a 6+ you find something stuck inside! Add <b>1 Broken Lantern</b> basic resource to the settlement's storage.",
        'type': 'strange_resources',
        'name': 'Lantern Tube',
        'keywords': ['organ', 'scrap']
    },
    'leather': {
        'type': 'strange_resources',
        'name': 'Leather',
        'keywords': ['hide'],
        'desc': 'Never goes out of style.',
    },
    'legendary_horns': {
        'type': 'strange_resources',
        'name': 'Legendary Horns',
        'keywords': ['bone', 'scrap'],
        'desc': 'Holding them fills you with power.',
    },
    'perfect_crucible': {
        'type': 'strange_resources',
        'name': 'Perfect Crucible',
        'keywords': ['iron'],
        'desc': 'When you craft with Perfect Crucible, an ancient bacteria is released into the air. Suffer -1d10 population and archive this card.',
    },
    'phoenix_crest': {
        'type': 'strange_resources',
        'name': 'Phoenix Crest',
        'keywords': ['organ'],
        'desc': 'Firm and supple.',
    },
    'second_heart': {
        'type': 'strange_resources',
        'name': 'Second Heart',
        'keywords': ['organ', 'bone'],
        'desc': 'It still tries to bite you.',
    },

    # screaming antelope
    'beast_steak': {
        'type': 'screaming_antelope_resources',
        'name': 'Beast Steak',
        'keywords': ['organ','consumable'],
        'desc': '<i>Shockingly appetizing.</i>',
    },
    'bladder': {
        'type': 'screaming_antelope_resources',
        'name': 'Bladder',
        'keywords': ['organ','consumable'],
        'desc': '<i>Smells like urine.</i>',
    },
    'large_flat_tooth': {
        'type': 'screaming_antelope_resources',
        'name': 'Large Flat Tooth',
        'keywords': ['bone'],
        'desc': 'When you gain this, a survivor of your choice gains +1 insanity.<br/><i>Its surface is rough and bumpy.</i>',
    },
    'muscly_gums': {
        'type': 'screaming_antelope_resources',
        'name': 'Muscly Gums',
        'keywords': ['organ','consumable'],
        'desc': '<i>Difficult to pry apart.</i>',
    },
    'pelt': {
        'type': 'screaming_antelope_resources',
        'name': 'Pelt',
        'keywords': ['hide'],
        'desc': '<i>Coarse and warm.</i>',
    },
    'screaming_brain': {
        'type': 'screaming_antelope_resources',
        'name': 'Screaming Brain',
        'keywords': ['organ','consumable'],
        'desc': '<b>Consume:</b> Archive this and gain survival up to the current limit.',
    },
    'shank_bone': {
        'type': 'screaming_antelope_resources',
        'name': 'Shank Bone',
        'keywords': ['bone'],
        'desc': '<i>Strangely jointed.</i>',
    },
    'spiral_horn': {
        'type': 'screaming_antelope_resources',
        'name': 'Spiral Horn',
        'keywords': ['bone'],
        'desc': '<i>Moans balefully when blown.</i>',
    },

    # phoenix
    'bird_beak': {
        'type': 'phoenix_resources',
        'name': 'Bird Beak',
        'keywords': ['bone'],
        'desc': '<i>Surprisingly toothy.</i>',
    },
    'black_skull': {
        'type': 'phoenix_resources',
        'name': 'Black Skull',
        'keywords': ['iron', 'skull', 'bone'],
        'desc': '<i>Aged to perfection.</i>',
    },
    'hollow_wing_bones': {
        'type': 'phoenix_resources',
        'name': 'Hollow Wing Bones',
        'keywords': ['bone'],
        'desc': '<i>Delicate and finely balanced.</i>',
    },
    'muculent_droppings': {
        'type': 'phoenix_resources',
        'name': 'Muculent Droppings',
        'keywords': ['organ'],
        'desc': '<i>Delicately scented, papery husk</i>',
    },
    'phoenix_eye': {
        'type': 'phoenix_resources',
        'name': 'Phoenix Eye',
        'keywords': ['organ', 'scrap'],
        'desc': '<i>Filled with a thick, metallic liquid.',
    },
    'phoenix_finger': {
        'type': 'phoenix_resources',
        'name': 'Phoenix Finger',
        'keywords': ['bone'],
        'desc': 'When you gain this, a survivor of your choice gains +3 insanity.',
    },
    'phoenix_whisker': {
        'type': 'phoenix_resources',
        'name': 'Phoenix Whisker',
        'keywords': ['hide'],
        'desc': '<i>Silky, yet robust.</i>',
    },
    'pustules': {
        'type': 'phoenix_resources',
        'name': 'Pustules',
        'keywords': ['organ','consumable'],
        'desc': '<i>The aroma is tempting.</i>',
    },
    'rainbow_droppings': {
        'type': 'phoenix_resources',
        'name': 'Rainbow Droppings',
        'keywords': ['organ','consumable'],
        'desc': '<b>Consume:</b> Archive this and roll 1d10. On 7+, gain +1 permanent speed. Otherwise, your heart explodes, killing you instantly.',
    },
    'shimmering_halo': {
        'type': 'phoenix_resources',
        'name': 'Shimmering Halo',
        'keywords': ['organ'],
        'desc': '<i>Curiously heavy.</i>',
    },
    'small_feathers': {
        'type': 'phoenix_resources',
        'name': 'Small Feathers',
        'keywords': ['hide'],
        'desc': '<i>Soft interior with razor sharp edges.</i>',
    },
    'small_hand_parasites': {
        'type': 'phoenix_resources',
        'name': 'Small Hand Parasites',
        'keywords': ['organ'],
        'desc': '<i>Still wriggling.</i>',
    },
    'tail_feathers': {
        'type': 'phoenix_resources',
        'name': 'Tail Feathers',
        'keywords': ['hide'],
        'desc': '<i>Lighter than air.</i>',
    },
    'wishbone': {
        'type': 'phoenix_resources',
        'name': 'Wishbone',
        'keywords': ['bone'],
        'desc': '<i>A delicate bone with a strange aura.</i>',
    },

    # white lion
    'curious_hand': {
        'type': 'white_lion_resources',
        'name': 'Curious Hand',
        'keywords': ['hide'],
        'desc': 'When you gain this, a random survivor gains +1 insanity.<br/><i>Holding this fills you with sadness.</i>',
    },
    'eye_of_cat': {
        'type': 'white_lion_resources',
        'name': 'Eye of Cat',
        'keywords': ['organ','consumable'],
        'desc': '<i>A perfectly preserved eye.</i>',
    },
    'golden_whiskers': {
        'type': 'white_lion_resources',
        'name': 'Golden Whiskers',
        'keywords': ['organ'],
        'desc': '<i>These whiskers are tough!</i>',
    },
    'great_cat_bones': {
        'type': 'white_lion_resources',
        'name': 'Great Cat Bones',
        'keywords': ['bone'],
        'desc': 'Strong and surprisingly light.',
    },
    'lion_claw': {
        'type': 'white_lion_resources',
        'name': 'Lion Claw',
        'keywords': ['bone'],
        'desc': '<i>A razor-sharp, retractable claw.</i>',
    },
    'lion_tail': {
        'type': 'white_lion_resources',
        'name': 'Lion Tail',
        'keywords': ['hide'],
        'desc': "<i>It's surprisingly heavy.</i>",
    },
    'lion_testes': {
        'type': 'white_lion_resources',
        'name': 'Lion Testes',
        'keywords': ['organ','consumable'],
        'desc': '<i>A hefty pair of nuts.</i>',
    },
    'shimmering_mane': {
        'type': 'white_lion_resources',
        'name': 'Shimmering Mane',
        'keywords': ['hide'],
        'desc': 'Archive this to gain 2 basic hide resources.<br/><i>It shimmers in the lantern light.</i>',
    },
    'sinew': {
        'type': 'white_lion_resources',
        'name': 'Sinew',
        'keywords': ['organ'],
    },
    'white_fur': {
        'type': 'white_lion_resources',
        'name': 'White Fur',
        'keywords': ['hide'],
        'desc': '<i>Luxurious and soft to the touch.</i>',
    },
}


vermin = {
    'crab_spider': {
        'type': 'vermin',
        'name': 'Crab Spider',
        'desc': '<b>Consume:</b> Archive this and gain +3 survival.',
        'keywords': ['hide','vermin','consumable'],
    },
    'cyclops_fly': {
        'type': 'vermin',
        'name': 'Cyclops Fly',
        'desc': '<b>Consume:</b> Archive this and roll 1d10.',
        'keywords': ['vermin','consumable'],
    },
    'hissing_cockroach': {
        'type': 'vermin',
        'name': 'Hissing Cockroach',
        'keywords': ['vermin','consumable'],
        'desc': '<b>Consume:</b> Archive this to lose all survival and gain 2d10 insanity.<br/>If you are insane, you must consume this.',
    },
    'lonely_ant': {
        'type': 'vermin',
        'name': 'Lonely Ant',
        'keywords': ['vermin','consumable'],
        'desc': '<b>Consume:</b> Archive this to swap your insanity and survival values.',
    },
    'nightmare_tick': {
        'type': 'vermin',
        'name': 'Nightmare Tick',
        'keywords': ['vermin','consumable'],
        'desc': '<b>Consume:</b> Archive this and roll 1d10.',
    },
    'sword_beetle': {
        'type': 'vermin',
        'name': 'Sword Beetle',
        'desc': '<b>Consume:</b> Archive this and roll 1d10.',
        'keywords': ['vermin','consumable'],
    },
}


expansions = {

    #gorm strange resources
    'active_thyroid': {
        'expansion': 'gorm',
        'type': 'strange_resources',
        'name': 'Active Thyroid',
        'keywords': ['organ','consumable'],
        'desc': '<b>Consume:</b> archive this and roll 1d10. On a 7+, gain +1 permanent speed. Otherwise, your heart explodes, killing you instantly.',
    },
    'gormite': {
        'expansion': 'gorm',
        'type': 'strange_resources',
        'name': 'Gormite',
        'keywords': ['scrap', 'iron'],
        'desc': '<i>The toughest stuff known to man.</i>',
    },
    'pure_bulb': {
        'expansion': 'gorm',
        'type': 'strange_resources',
        'name': 'Pure Bulb',
        'keywords': ['organ'],
        'desc': "<i>Don't stare at it.</i>",
    },
    'stomach_lining': {
        'expansion': 'gorm',
        'type': 'strange_resources',
        'name': 'Stomach Lining',
        'keywords': ['organ'],
        'desc': '<i>Steadily expands and contracts.</i>',
    },

    # gorm resources
    'acid_gland': {
        'expansion': 'gorm',
        'type': 'gorm_resources',
        'name': 'Acid Gland',
        'keywords': ['organ'],
        'desc': '<i>Melts skin.</i>',
    },
    'dense_bone': {
        'expansion': 'gorm',
        'type': 'gorm_resources',
        'name': 'Dense Bone',
        'keywords': ['bone'],
        'desc': '<i>Sturdy.</i>',
    },
    'gorm_brain': {
        'expansion': 'gorm',
        'type': 'gorm_resources',
        'name': 'Gorm Brain',
        'keywords': ['organ'],
        'desc': '<i>Shockingly small.</i>',
    },
    'handed_skull': {
        'expansion': 'gorm',
        'type': 'gorm_resources',
        'name': 'Handed Skull',
        'keywords': ['bone'],
        'desc': '<i>Incomparably dense.</i>',
    },
    'jiggling_lard': {
        'expansion': 'gorm',
        'type': 'gorm_resources',
        'name': 'Jiggling Lard',
        'keywords': ['organ','hide'],
        'desc': '<i>Thick, quivering mass.</i>',
    },
    'mammoth_hand': {
        'expansion': 'gorm',
        'type': 'gorm_resources',
        'name': 'Mammoth Hand',
        'keywords': ['bone', 'hide', 'organ'],
        'desc': '<i>An enormous, leathery glove.</i>',
    },
    'meaty_rib': {
        'expansion': 'gorm',
        'type': 'gorm_resources',
        'name': 'Meaty Rib',
        'keywords': ['bone', 'organ'],
        'desc': '<i>Useful and delicious.</i>',
    },
    'milky_eye': {
        'expansion': 'gorm',
        'type': 'gorm_resources',
        'name': 'Milky Eye',
        'keywords': ['organ'],
        'desc': '<i>When this resource is gained, select a survivor to gain +3 insanity.</i>',
    },
    'stout_heart': {
        'expansion': 'gorm',
        'type': 'gorm_resources',
        'name': 'Stout Heart',
        'keywords': ['organ'],
        'desc': '<i>A titanic pump.</i>',
    },
    'stout_hide': {'expansion': 'gorm',
        'type': 'gorm_resources',
        'name': 'Stout Hide',
        'keywords': ['hide'],
        'desc': '<i>Tough, wrinkly skin.</i>',
    },
    'stout_kidney': {
        'expansion': 'gorm',
        'type': 'gorm_resources',
        'name': 'Stout Kidney',
        'keywords': ['organ'],
        'desc': '<b>Consume:</b> archive this and roll 1d10. On a result of 6+, gain 10 survival. Otherwise, reduce your survival to 0.',
    },
    'stout_vertebrae': {
        'expansion': 'gorm',
        'type': 'gorm_resources',
        'name': 'Stout Vertebrae',
        'keywords': ['bone'],
        'desc': '<i>Hefty and intricately jointed.</i>',
    },


    # spidicules strange resources
    'silken_nervous_system': {
        'expansion': 'spidicules',
        'type': 'strange_resources',
        'name': 'Silken Nervous System',
        'keywords': ['organ'],
        'desc': '<i>Separates into tiny golden threads.</i>',
    },
    'web_silk': {
        'expansion': 'spidicules',
        'type': 'strange_resources',
        'name': 'Web Silk',
        'keywords': ['silk'],
        'desc': '<i>Impossible to tear.</i>',
    },

    # spidicules resources
    'arachnid_heart': {
        'expansion': 'spidicules',
        'type': 'spidicules_resources',
        'name': 'Arachnid Heart',
        'keywords': ['organ'],
        'desc': '<i>Cold to the touch, even when freshly removed.</i>',
    },
    'chitin': {
        'expansion': 'spidicules',
        'type': 'spidicules_resources',
        'name': 'Chitin',
        'keywords': ['hide'],
        'desc': '<i>A flaky, bitter-smelling husk.</i>',
    },
    'exoskeleton': {
        'expansion': 'spidicules',
        'type': 'spidicules_resources',
        'name': 'Exoskeleton',
        'keywords': ['hide'],
        'desc': '<i>Malleable, interlocking plates.</i>',
    },
    'eyeballs': {
        'expansion': 'spidicules',
        'type': 'spidicules_resources',
        'name': 'Eyeballs',
        'keywords': ['organ'],
        'desc': '<i>Each points in a different direction.</i>',
    },
    'large_appendage': {
        'expansion': 'spidicules',
        'type': 'spidicules_resources',
        'name': 'Large Appendage',
        'keywords': ['bone'],
        'desc': '<i>Could come in handy.</i>',
    },
    'serrated_fangs': {
        'endeavors': ['serrated_fangs_razor_pushups'],
        'expansion': 'spidicules',
        'type': 'spidicules_resources',
        'name': 'Serrated Fangs',
        'keywords': ['bone'],
    },
    'small_appendages': {
        'expansion': 'spidicules',
        'type': 'spidicules_resources',
        'name': 'Small Appendages',
        'keywords': ['hide'],
        'desc': '<i>The inner hands look surprisingly human.</i>',
    },
    'spinnerets': {
        'expansion': 'spidicules',
        'type': 'spidicules_resources',
        'name': 'Spinnerets',
        'keywords': ['organ', 'scrap'],
        'desc': '<i>More complex than any device.</i>',
    },
    'stomach': {
        'expansion': 'spidicules',
        'type': 'spidicules_resources',
        'name': 'Stomach',
        'keywords': ['organ'],
        'desc': '<b>Consume:</b> Archive this card to gain +1 Hunt XP.',
    },
    'thick_web_silk': {
        'expansion': 'spidicules',
        'type': 'spidicules_resources',
        'name': 'Thick Web Silk',
        'keywords': ['silk','hide'],
        'desc': '<i>Impossible to pierce.</i>',
    },
    'unlaid_eggs': {
        'expansion': 'spidicules',
        'type': 'spidicules_resources',
        'name': 'Unlaid Eggs',
        'keywords': ['organ','consumable'],
        'desc': 'During the settlement phase, you may <b>consume</b> and archive these delicious little eggs to gain 10 survival.',
    },
    'venom_sac': {
        'expansion': 'spidicules',
        'type': 'spidicules_resources',
        'name': 'Venom Sac',
        'keywords': ['organ', 'consumable'],
        'desc': '<b>Consume:</b> Archive this card and roll 1d10. On a 1-5, you die instantly. On a 6+, gain the <b>Death Touch</b> Secret Fighting Art.',
    },


    # dung_beetle_knight strange resources
    'preserved_caustic_dung': {
        'expansion': 'dung_beetle_knight',
        'type': 'strange_resources',
        'name': 'Preserved Caustic Dung',
        'keywords': ['organ','consumable','dung'],
        'desc': 'The live cultures in this exotic mixture of matured dung have been preserved within a delicate, airtight jelly casing.',
    },
    'scell': {
        'expansion': 'dung_beetle_knight',
        'type': 'strange_resources',
        'name': 'Scell',
        'keywords': ['organ','consumable'],
        'desc': "As the monster ages, this sticky and corrosive material builds between the thin layers of its scarab shells. It breaks down fecal product, preventing the knight's joints from locking up.<br/>During <b>Black Harvest</b>, a Restorer can make excellent use of a Scell, using it to nearly perfect the final step of the calcification process.",
    },

    # dung_beetle_knight resources 

    'beetle_horn': {
        'expansion': 'dung_beetle_knight',
        'type': 'dung_beetle_knight_resources',
        'name': 'Beetle Horn',
        'keywords': ['bone'],
        'endeavors': ['dbk_horn_ceremony'],
    },
    'century_fingernails': {
        'expansion': 'dung_beetle_knight',
        'type': 'dung_beetle_knight_resources',
        'name': 'Century Fingernails',
        'keywords': ['bone'],
        'desc': 'These nails are never clipped. Instead, they are folded and hammered hundreds of times into an impossibly fine edge.',
    },
    'century_shell': {
        'expansion': 'dung_beetle_knight',
        'type': 'dung_beetle_knight_resources',
        'name': 'Century Shell',
        'keywords': ['hide', 'iron'],
        'desc': 'This ancient and mineral-rich armor plate is covered with razor wind scratches.<br/>You may spend this as if it were a <b>Scarab Shell</b> resources.',
    },
    'compound_eye': {
        'expansion': 'dung_beetle_knight',
        'type': 'dung_beetle_knight_resources',
        'name': 'Compound Eye',
        'keywords': ['organ','consumable'],
        'desc': 'A cluster of differently colored eyes, each filled with a creamy, tangy syrup. If you have 3+ courage, you may <b>consume</b> and archive this to gain +3d10 insanity.',
    },
    'elytra': {
        'expansion': 'dung_beetle_knight',
        'type': 'dung_beetle_knight_resources',
        'name': 'Elytra',
        'keywords': ['bone', 'hide', 'organ'],
        'desc': 'The ribbed underside of these large shells makes an ideal surface to grind weapons. A survivor may archive this to give all of their attacks in the next showdown <b>Sharp</b>.',
    },
    'scarab_shell': {
        'expansion': 'dung_beetle_knight',
        'type': 'dung_beetle_knight_resources',
        'name': 'Scarab Shell',
        'keywords': ['hide'],
        'desc': 'Cool and oily to the touch. Lantern light reveals a brilliant band of color dancing on its surface.',
    },
    'scarab_wing': {
        'expansion': 'dung_beetle_knight',
        'type': 'dung_beetle_knight_resources',
        'name': 'Scarab Wing',
        'keywords': ['organ'],
        'desc': 'When soaked in water, these vein-filled wings gain some elasticity.',
    },
    'underplate_fungus': {
        'expansion': 'dung_beetle_knight',
        'type': 'dung_beetle_knight_resources',
        'name': 'Underplate Fungus',
        'keywords': ['herb', 'hide', 'consumable'],
        'desc': "A corkscrew-shaped fungus that grows in the empty channels between the Dung Beetle Knight's armor plating.",
    },


    # sunstalker strange resources
    '1000_year_sunspot': {
        'expansion': 'sunstalker',
        'type': 'strange_resources',
        'name': '1,000 Year Sunspot',
        'keywords': ['bone', 'organ'],
        'desc': 'When you craft with this, nominate a survivor. They suffer the <b>blind</b> severe injury from working with this resource.',
    },
    '3000_year_sunspot': {
        'expansion': 'sunstalker',
        'type': 'strange_resources',
        'name': '3,000 Year Sunspot',
        'keywords': ['bone', 'organ', 'scrap'],
        'desc': 'When you craft with this, nominate a survivor and roll 1d10. On a 5+ they get a terrible headache and die.',
    },
    'bugfish': {
        'expansion': 'sunstalker',
        'type': 'strange_resources',
        'name': 'Bugfish',
        'keywords': ['fish','organ'],
        'desc': '<b>Consume:</b> Gain +2 survival. There is something in its belly! Gain 1 random vermin and <b>consume</b> it immediately. Archive this card.',
    },
    'salt': {
        'expansion': 'sunstalker',
        'type': 'strange_resources',
        'name': 'Salt',
        'desc': "You may add this to any cooking recipe to gain +1 permanent strength in addition to the recipe's listed benefits.<br/><i>When exposed to lantern light it evaporates, forming a crust</i>.",
    },
    'sunstones': {
        'expansion': 'sunstalker',
        'type': 'strange_resources',
        'name': 'Sunstones',
        'misspellings': ['Sun Stones'],
        'keywords': ['bone'],
        'desc': 'Small and warm.',
    },
    'hagfish': {
        'expansion': 'sunstalker',
        'type': 'strange_resources',
        'name': 'Hagfish',
        'keywords': ['bone', 'hide'],
        'desc': '<b>Consume:</b> Your hair turns gray and you gain +1 Hunt XP. Archive this card.',
    },
    'jowls': {
        'expansion': 'sunstalker',
        'type': 'strange_resources',
        'name': 'Jowls',
        'keywords': ['fish','iron'],
        'desc': "When you gain Jowls, it bites off your nose! If you have no nose, you die.<br/>If you have <b>Jowls</b>, <b>Hagfish</b>, and <b>Bugfish</b>, you are inspired! You may archive all 3 to gain the <b>Filleting Table</b> innovation.",
    },

    # sunstalker resources
    'black_lens': {
        'expansion': 'sunstalker',
        'type': 'sunstalker_resources',
        'name': 'Black Lens',
        'keywords': ['organ'],
        'desc': '<i>These eyes are filled with a savory, gluey substance that dries when exposed to air.<i>',
    },
    'brain_root': {
        'expansion': 'sunstalker',
        'type': 'sunstalker_resources',
        'name': 'Brain Root',
        'keywords': ['organ'],
        'desc': '<i>The strands of the root are strong and elastic. The meat on top is useless.</i>',
    },
    'cycloid_scales': {
        'expansion': 'sunstalker',
        'type': 'sunstalker_resources',
        'name': 'Cycloid Scales',
        'keywords': ['hide'],
        'desc': '<i>Extremely reflective and colorful.</i>',
    },
    'fertility_tentacle': {
        'expansion': 'sunstalker',
        'type': 'sunstalker_resources',
        'name': 'Fertility Tentacle',
        'keywords': ['organ'],
        'desc': '<i>This tube-like appendage has a cavity at the base that stores eggs.</i>',
    },
    'huge_sunteeth': {
        'expansion': 'sunstalker',
        'type': 'sunstalker_resources',
        'name': 'Huge Sunteeth',
        'keywords': ['bone'],
        'desc': '<i>These tough but light teeth are made of hundreds of thin layers of bone, separated by rows of dicot stems.</i>',
    },
    'inner_shadow_skin': {
        'expansion': 'sunstalker',
        'type': 'sunstalker_resources',
        'name': 'Inner Shadow Skin',
        'keywords': ['hide'],
        'desc': '<i>This soft, yet rubbery material blocks light.</i>',
    },
    'prismatic_gills': {
        'expansion': 'sunstalker',
        'type': 'sunstalker_resources',
        'name': 'Prismatic Gills',
        'keywords': ['organ'],
        'desc': 'When you gain this, gain the <b>Emotionless</b> disorder.<br/><i>The gills emit a fuzzy color trail.</i>',
    },
    'shadow_ink_gland': {
        'expansion': 'sunstalker',
        'type': 'sunstalker_resources',
        'name': 'Shadow Ink Gland',
        'keywords': ['organ'],
        'desc': '<i>The ink can be used to paint shadows that vanish in lantern light.</i>',
    },
    'shadow_tentacles': {
        'expansion': 'sunstalker',
        'type': 'sunstalker_resources',
        'name': 'Shadow Tentacles',
        'keywords': ['organ', 'hide'],
        'desc': 'When you gain this during the hunt or showdown, return it to the resource deck and draw again if any survivors are <b>blind</b>.',
    },
    'shark_tongue': {
        'expansion': 'sunstalker',
        'type': 'sunstalker_resources',
        'name': 'Shark Tongue',
        'keywords': ['organ'],
        'desc': '<i>So slippery that its hard to hold!</i>',
    },
    'small_sunteeth': {
        'expansion': 'sunstalker',
        'type': 'sunstalker_resources',
        'name': 'Small Sunteeth',
        'keywords': ['bone'],
        'desc': '<i>Unlike the large sunteeth, these are extremely sharp and clean.</i>',
    },
    'stink_lung': {
        'expansion': 'sunstalker',
        'type': 'sunstalker_resources',
        'name': 'Stink Lung',
        'keywords': ['organ'],
        'desc': '<i>When squeezed, a funny noise emerges followed by a tantalizing aroma.</i>',
    },
    'sunshark_blubber': {
        'expansion': 'sunstalker',
        'type': 'sunstalker_resources',
        'name': 'Sunshark Blubber',
        'keywords': ['organ'],
        'desc': '<i>When inflated with air, this blubber gently floats.</i>',
    },
    'sunshark_bone': {
        'expansion': 'sunstalker',
        'type': 'sunstalker_resources',
        'name': 'Sunshark Bone',
        'keywords': ['bone'],
        'desc': '<i>The center is filled with water.</i>',
                   },
    'sunshark_fin': {
        'expansion': 'sunstalker',
        'type': 'sunstalker_resources',
        'name': 'Sunshark Fin',
        'keywords': ['bone', 'hide'],
        'desc': '<i>Removing the slimy hands reveals a curable, viscous substance.</i>',
    },


    # lonely_tree
    'blistering_plasma_fruit': {
        'expansion': 'lonely_tree',
        'type': 'strange_resources',
        'name': 'Blistering Plasma Fruit',
        'keywords': ['organ','consumable'],
    },
    'drifting_dream_fruit': {
        'expansion': 'lonely_tree',
        'type': 'strange_resources',
        'name': 'Drifting Dream Fruit',
        'keywords': ['consumable'],
    },
    'jagged_marrow_fruit': {
        'expansion': 'lonely_tree',
        'type': 'strange_resources',
        'name': 'Jagged Marrow Fruit',
        'keywords': ['bone', 'scrap','consumable']
    },
    'lonely_fruit': {
        'expansion': 'lonely_tree',
        'type': 'strange_resources',
        'name': 'Lonely Fruit',
        'keywords': ['consumable'],
    },
    'porous_flesh_fruit': {
        'expansion': 'lonely_tree',
        'type': 'strange_resources',
        'name': 'Porous Flesh Fruit',
        'keywords': ['hide','consumable'],
    },


    #dragon king strange resources
    'pituitary_gland': {
        'expansion': 'dragon_king',
        'type': 'strange_resources',
        'name': 'Pituitary Gland',
        'keywords': ['organ','consumable'],
        'desc': '<b>Consume:</b> Archive this and roll 1d10. On a 4+, gain +1 permanent strength. Otherwise, you grow to giant size and die.',
    },
    'radiant_heart': {
        'expansion': 'dragon_king',
        'type': 'strange_resources',
        'name': 'Radiant Heart',
        'keywords': ['organ'],
        'desc': 'When you gain this resource, roll 1d10. On a 3+ you burst into flames and die.',
    },
    'shining_liver': {
        'expansion': 'dragon_king',
        'type': 'strange_resources',
        'name': 'Shining Liver',
        'keywords': ['organ'],
        'desc': 'When exposed to light, it filters it into heat and become darker.',
    },

    # dragon king resources
    'cabled_vein': {
        'expansion': 'dragon_king',
        'type': 'dragon_king_resources',
        'name': 'Cabled Vein',
        'keywords': ['organ'],
        'desc': '<i>A dense bundle of bloody tubes.</i>',
    },
    'dragon_iron': {
        'expansion': 'dragon_king',
        'type': 'dragon_king_resources',
        'name': 'Dragon Iron',
        'keywords': ['iron'],
        'desc': '<i>It feels heavy, but when dropped, falls as slowly as a feather.</i>',
    },
    'hardened_ribs': {
        'expansion': 'dragon_king',
        'type': 'dragon_king_resources',
        'name': 'Hardened Ribs',
        'keywords': ['bone'],
        'desc': '<i>Strong, flexible, and hollow.</i>',
    },
    'horn_fragment': {
        'expansion': 'dragon_king',
        'type': 'dragon_king_resources',
        'name': 'Horn Fragment',
        'keywords': ['bone'],
        'desc': '<i>Nearby speech causes them to resonate.</i>',
    },
    'husk': {
        'expansion': 'dragon_king',
        'type': 'dragon_king_resources',
        'name': 'Husk',
        'keywords': ['hide'],
        'desc': '<i>A decaying layer of former skin.</i>',
    },
    "kings_claws": {'expansion': 'dragon_king',
        'type': 'dragon_king_resources',
        'name': "King's Claws",
        'keywords': ['bone'],
        'desc': '<i>Disturbingly warm, and sharp enough to draw blood with a touch.</i>',
    },
    "kings_tongue": {
        'expansion': 'dragon_king',
        'type': 'dragon_king_resources',
        'name': "King's Tongue",
        'keywords': ['hide'],
        'desc': '<i>Smooth, dry, and sharp.</i>',
    },
    'radioactive_dung': {
        'expansion': 'dragon_king',
        'type': 'dragon_king_resources',
        'name': 'Radioactive Dung',
        'keywords': ['organ', 'scrap'],
        'desc': '<i>Gives off smoke with an acrid odor.</i>',
    },
    'veined_wing': {
        'expansion': 'dragon_king',
        'type': 'dragon_king_resources',
        'name': 'Veined Wing',
        'keywords': ['hide'],
        'desc': '<i>Blood drips from it at a constant rate.</i>',
    },

    # lion_god
    'canopic_jar': {
        'expansion': 'lion_god',
        'type': 'strange_resources',
        'name': 'Canopic Jar',
        'keywords': ['organ', 'scrap'],
    },
    'old_blue_box': {
        'expansion': 'lion_god',
        'type': 'strange_resources',
        'name': 'Old Blue Box',
        'keywords': ['scrap'],
    },
    'sarcophagus': {
        'expansion': 'lion_god',
        'type': 'strange_resources',
        'name': 'Sarcophagus',
        'keywords': ['iron']
    },
    'silver_urn': {
        'expansion': 'lion_god',
        'type': 'strange_resources',
        'name': 'Silver urn',
        'keywords': ['bone', 'scrap'],
    },
    'triptych': {
        'expansion': 'lion_god',
        'type': 'strange_resources',
        'name': 'Triptych',
        'keywords': ['hide', 'scrap'],
    },


    # manhunter
    'crimson_vial': {
        'expansion': 'manhunter',
        'type': 'strange_resources',
        'name': 'Crimson Vial',
        'keywords': ['iron', 'consumable'],
        'desc': 'You may <b>consume</b> and archive this to remove all bleeding tokens and any severe injury of your choice.',
    },
    'red_vial': {
        'expansion': 'manhunter',
        'type': 'strange_resources',
        'name': 'Red Vial',
        'desc': 'You may <b>consume</b> and archive this to remove 2 bleeding tokens and gain +1 survival.',
        'keywords': ['consumable'],
    },

    # slenderman
    'crystal_sword_mold': {
        'expansion': 'slenderman',
        'type': 'strange_resources',
        'name': 'Crystal Sword Mold',
        'keywords': ['scrap','iron'],
    },
    'dark_water': {
        'expansion': 'slenderman',
        'type': 'strange_resources',
        'name': 'Dark Water',
        'keywords': ['other','consumable'],
        'desc': "You may <b>consume</b> and archive this to remove all your disorders, then gain a random disorder.",
    },

    # flower knight
    'lantern_bloom': {
        'expansion': 'flower_knight',
        'type': 'flower_knight_resources',
        'name': 'Lantern Bloom',
        'keywords': ['flower','hide'],
        'rules': ['Perishable'],
    },
    'lantern_bud': {
        'expansion': 'flower_knight',
        'type': 'flower_knight_resources',
        'name': 'Lantern Bud',
        'keywords': ['flower','scrap',],
        'rules': ['Perishable'],
    },
    'osseous_bloom': {
        'expansion': 'flower_knight',
        'type': 'flower_knight_resources',
        'name': 'Osseous Bloom',
        'keywords': ['flower','bone'],
        'rules': ['Perishable'],
    },
    'sighing_bloom': {
        'expansion': 'flower_knight',
        'type': 'flower_knight_resources',
        'name': 'Sighing Bloom',
        'keywords': ['flower','organ',],
        'rules': ['Perishable'],
    },
    'warbling_bloom': {
        'expansion': 'flower_knight',
        'type': 'flower_knight_resources',
        'name': 'Warbling Bloom',
        'keywords': ['flower','hide'],
        'rules': ['Perishable'],
    },

}


