#!/usr/bin/env python

#   standard
import Cookie
from datetime import datetime, timedelta
from string import Template
import sys

#   custom
import admin
from session import Session
from utils import load_settings, mdb, get_logger

settings = load_settings()
logger = get_logger()

user_error_msg = Template('<div id="user_error_msg" class="$err_class">$err_msg</div>')


class panel:
    headline = Template("""\n\
    <meta http-equiv="refresh" content="30">
    <table id="panel_meta_stats">
        <tr><th colspan="2">Global Stats</th></tr>
        <tr><td>Total Users:</td><td>$users</td></tr>
        <tr class="grey"><td>Recent Users:</td><td>$recent_users_count</td></tr>
        <tr><td>Sessions:</td><td>$sessions</td></tr>
        <tr class="grey"><td>Settlements:</td><td>$settlements</td></tr>
        <tr><td>Survivors:</td><td>$live_survivors/$dead_survivors ($total_survivors total)</td></tr>
        <tr class="grey"><td>Valkyrie:</td><td>$complete_death_records complete death recs</td></tr>
        <tr><td>Latest Fatality:</td><td>$latest_fatality</td></tr>
    </table>
    \n""")
    log_line = Template("""\n\
    <p class="$zebra">$line</p>
    \n""")
    user_status_summary = Template("""\n\
    <div class="panel_block">
        <table class="panel_recent_user">
            <tr class="gradient_blue bold"><th colspan="3">$user_name</th></tr>
            <tr><td>Latest Activity:</td><td>$latest_activity</td><td>$latest_activity_mins m. ago: $latest_action</td></tr>
            <tr><td>Latest Sign-in:</td><td>$latest_sign_in</td><td>$latest_sign_in_mins m. ago</td></tr>
            <tr><td>Session Length:</td><td colspan="2">$session_length minutes</td></tr>
            <tr><td>User Agent:</td><td colspan="2">$ua</td></tr>
            <tr><td>Survivors:</td><td colspan="2">$survivor_count</td></tr>
            <tr><td>Settlements:</td><td colspan="2">$settlements</td></tr>
        </table>
    </div><br/>
    \n""")


class ui:
    game_asset_select_top = Template("""\n\
    <select name="$operation$name" onchange="this.form.submit()">
    <option selected disabled hidden value="">$operation_pretty $name_pretty</option>
    """)
    game_asset_select_row = Template('\t  <option value="$asset">$asset</option>\n')
    game_asset_select_bot = '    </select>\n'
    game_asset_add_custom = Template("""\n\
<input onchange="this.form.submit()" type="text" class="full_width" name="add_$asset_name" placeholder="add custom $asset_name"/>
    \n""")
    text_input = Template('\t  <input onchange="this.form.submit()" type="text" class="full_width" name="$name" placeholder="$placeholder_text"/>')


class dashboard:
    # settlement administrivia; needs to be above the dashboard accordions
    panel_button = '<hr class="mobile_only"/><form method="POST"><input type="hidden" name="change_view" value="panel"/><button class="maroon change_view">Admin Panel!</button></form>\n'
    new_settlement_button = '<form method="POST"><input type="hidden" name="change_view" value="new_settlement" /><button class="success">+ New Settlement</button></form>\n'

    # flash
    down_arrow_flash = '<img class="dashboard_down_arrow" src="%s/icons/down_arrow.png"/> ' % settings.get("application", "STATIC_URL")
    campaign_flash = '<img class="dashboard_icon" src="%s/icons/campaign.png"/> ' % settings.get("application", "STATIC_URL")
    settlement_flash = '<img class="dashboard_icon" src="%s/icons/settlement.png"/> ' % settings.get("application", "STATIC_URL")
    system_flash = '<img class="dashboard_icon" src="%s/icons/system.png"/> ' % settings.get("application", "STATIC_URL")
    refresh_flash = '<img class="dashboard_icon" src="%s/icons/refresh.png"/> ' % settings.get("application", "STATIC_URL")

    # dashboard accordions
    motd = Template("""\n
    <div class="dashboard_menu">
        <h2 class="clickable gradient_silver" onclick="showHide('system_div')"> <img class="dashboard_icon" src="%s/icons/system.png"/> System %s</h2>
        <div id="system_div" style="display: none;" class="dashboard_accordion gradient_silver">
        <p>KD:M Manager! Version $version.</p><hr/>
        <p>This application is a work in progress and is currently running in debug mode! Please use <a href="http://blog.kdm-manager.com"/>blog.kdm-manager.com</a> to report issues/bugs or to ask questions, share ideas for features, make comments, etc.</p>
        <hr/>


        <div class="dashboard_preferences">
            <h3>Preferences</h3>
            <form method="POST" action="#">
            <input type="hidden" name="update_user_preferences" value="True"/>
            <p>Confirm before removing items from storage?</p>
            <p>
                <input style="display: none" id="pref_confirm_on_remove" class="radio_principle" type="radio" name="confirm_on_remove_from_storage" value="confirm" checked/> <label for="pref_confirm_on_remove" class="radio_principle_label">Confirm</label><br>
                <input style="display: none" id="pref_do_not_confirm_on_remove" class="radio_principle" type="radio" name="confirm_on_remove_from_storage" value="do_not_confirm" $preferences_confirm_on_remove /> <label for="pref_do_not_confirm_on_remove" class="radio_principle_label">Do Not Confirm</label> 
            </p>
            <button class="warn"> Update Preferences</button>
            </form>
        </div>

        <hr/>

        <div class="dashboard_preferences">
            <h3>Export User Data</h3>
            <form method="POST" action="#">
                <input type="hidden" name="export_user_data" value="json">
                <button class="silver">JSON</button>
            </form>
            <form method="POST" action="#">
                <input type="hidden" name="export_user_data" value="dict">
                <button class="silver">Python Dictionary</button>
            </form>
            <form method="POST" action="#">
                <input type="hidden" name="export_user_data" value="pickle">
                <button class="silver">Python Pickle</button>
            </form>
        </div>

        <hr>

        <p>Currently signed in as: <i>$login</i> (last sign in: $last_sign_in)</p>
        $last_log_msg
        <div class="dashboard_preferences">
            <form method="POST">
            <input type="hidden" name="change_password" value="True"/>
            <input type="password" name="password" class="full_width" placeholder="password">
            <input type="password" name="password_again" class="full_width" placeholder="password (again)"/>
            <button class="warn"> Change Password</button>
            </form>
        </div>
        <hr class="desktop_only">
        <form id="logout" method="POST"><input type="hidden" name="remove_session" value="$session_id"/><input type="hidden" name="login" value="$login"/><button class="warn change_view desktop_only">SIGN OUT</button>\n\t</form>
        </div>
    </div>
    """ % (settings.get("application", "STATIC_URL"), down_arrow_flash))
    campaign_summary = Template("""\n\
    <div class="dashboard_menu">
        <h2 class="clickable gradient_purple" onclick="showHide('campaign_div')"> <img class="dashboard_icon" src="%s/icons/campaign.png"/> Campaigns %s </h2>
        <div id="campaign_div" style="display: $display" class="dashboard_accordion gradient_purple">
        <p>Games you are currently playing.</p>
            <div class="dashboard_button_list">
            $campaigns
            </div>
        </div>
    </div>
    \n""" % (settings.get("application", "STATIC_URL"), down_arrow_flash))
    settlement_summary = Template("""\n\
    <div class="dashboard_menu">
        <h2 class="clickable gradient_orange" onclick="showHide('settlement_div')"> <img class="dashboard_icon" src="%s/icons/settlement.png"/> Settlements %s </h2>
        <div id="settlement_div" style="display: $display" class="dashboard_accordion gradient_orange">
        <p>Manage your settlements. You may not manage a settlement you did not create.</p>
        <div class="dashboard_button_list">
            $settlements
            %s
        </div>
        </div>
    </div>
    \n""" % (settings.get("application", "STATIC_URL"), down_arrow_flash, new_settlement_button))
    survivor_summary = Template("""\n\
    <div class="dashboard_menu">
        <h2 class="clickable gradient_green" onclick="showHide('survivors_div')"> <img class="dashboard_icon" src="%s/icons/survivor.png"/> Survivors %s</h2>
        <div id="survivors_div" style="display: none;" class="dashboard_accordion gradient_green">
        <p>Manage survivors created by you or shared with you. New survivors are created from the "Campaign" and "Settlement" views.</p>
        <div class="dashboard_button_list">
            $survivors
        </div>
        </div>
    </div>
    \n""" % (settings.get("application", "STATIC_URL"), down_arrow_flash))
    world = Template("""\n
    <div class="dashboard_menu">
        <h2 class="clickable gradient_blue" onclick="showHide('world_div')"> <img class="dashboard_icon" src="%s/icons/world.png"/> World %s</h2>
        <div id="world_div" style="display: none;" class="dashboard_accordion gradient_blue">
        <p>$total_users users are managing $total_settlements settlements in $total_sessions sessions.</p><hr/>
        <p>$live_survivors survivors are alive and fighting; $dead_survivors have perished.</p><hr/>
        <p>Latest fatality:<br/>
        &ensp; <b>$dead_name</b> of <b>$dead_settlement</b><br/>
        &ensp; <i>$cause_of_death</i><br/>
        &ensp; Died in LY $dead_ly, XP: $dead_xp<br/>
        &ensp; Courage: $dead_courage, Understanding: $dead_understanding
        </p>
        </div>
    </div>
    """ % (settings.get("application", "STATIC_URL"), down_arrow_flash))

    # misc html assets
    home_button = '<form method="POST" action="#"><input type="hidden" name="change_view" value="dashboard"/><button id="floating_dashboard_button" class="gradient_silver"> %s <span class="desktop_only">Return to Dashboard</span></button></form>\n' % system_flash
    refresh_button = '<form method="POST" action="#"><button id="floating_refresh_button" class=""> %s </button></form>\n' % refresh_flash
    view_asset_button = Template("""\n\
    <form method="POST" action="#">
    <input type="hidden" name="view_$asset_type" value="$asset_id" />
    <button id="$button_id" class="$button_class" $disabled>$asset_name <span class="desktop_only">$desktop_text</span></button>
    </form>
    \n""")





class survivor:
    no_survivors_error = '<!-- No Survivors Found! -->'
    new = Template("""\n\
    <span class="desktop_only nav_bar gradient_green"></span>
    <br class="desktop_only"/>
    <div id="create_new_asset_form_container">
        <h3>Create a New Survivor!</h3>
        <form method="POST" action="#">
        <input type="hidden" name="new" value="survivor" />
        <input type="hidden" name="settlement_id" value="$home_settlement">
        <input type="text" name="name" placeholder="Survivor Name"/ class="full_width" autofocus>
        <input type="text" name="email" placeholder="Survivor Email"/ class="full_width" value="$user_email">
        <div id="block_group">
        <h2>Survivor Sex</h2>
            <fieldset class="radio">
          <input type="radio" id="male_button" class="radio_principle" name="sex" value="Male" checked/> 
          <label class="radio_principle_label" for="male_button"> Male </label><br/>
          <input type="radio" id="female_button" class="radio_principle" name="sex" value="Female"/> 
          <label class="radio_principle_label" for="female_button"> Female </label>
            </fieldset>
        </div>
        <div class="create_new_asset_block">
            $add_ancestors
            <button class="success">SAVE</button>
            </form>
        </div>
    </div>
    \n""")
    add_ancestor_top = '    <div id="block_group">\n    <h2>Survivor Parents</h2>\n'
    add_ancestor_select_top = Template('\t<select name="$parent_role">\n\t<option selected disabled hidden value="">$pretty_role</option>')
    add_ancestor_select_row = Template('\t<option value="$parent_id">$parent_name</option>\n')
    add_ancestor_select_bot = '\t</select><br class="mobile_only"/><br class="mobile_only"/>'
    add_ancestor_bot = '    </div>\n'
    campaign_summary_hide_show = Template("""\n\
    <h3 class="clickable $color align_left" onclick="showHide('$group_id')">$heading ($death_count) <img class="dashboard_down_arrow" src="%s/icons/down_arrow.png"/> </h3>
    <div id="$group_id" style="display: none;">
        $dead_survivors
    </div> <!-- deadSurvivorsBlock -->
    \n""" % (settings.get("application","STATIC_URL")))
    campaign_asset = Template("""\n\
      <div class="survivor_campaign_asset_container">

        <form method="POST" action="#edit_hunting_party">
         <input type="hidden" name="modify" value="survivor" />
         <input type="hidden" name="asset_id" value="$survivor_id" />
         <input type="hidden" name="view_game" value="$settlement_id" />
         <input type="hidden" name="in_hunting_party" value="$hunting_party_checked"/>
         <button id="add_survivor_to_party" class="$able_to_hunt" $able_to_hunt $disabled>::</button>
        </form>

        <form method="POST" action="#">
         <input type="hidden" name="view_survivor" value="$survivor_id" />
         <button id="survivor_campaign_asset" class="$b_class" $disabled>
            <center> <font class="$favorite"/>&#9733;</font> <b>$name</b> [$sex] </center>
            $special_annotation
            &ensp; XP: $hunt_xp &ensp; Survival: $survival<br/>
            &ensp; Insanity: $insanity <br/>
            &ensp; Courage: $courage<br/>
            &ensp; Understanding: $understanding
         </button>
        </form>
      </div>
      <hr class="invisible"/>
    \n""")
    form = Template("""\n\
    <span class="desktop_only nav_bar gradient_green"></span>
    <br class="desktop_only"/>
    $campaign_link

    <form method="POST" id="autoForm" action="#">
        <button id="save_button" class="success">Save</button>
        <input type="hidden" name="form_id" value="survivor_top" />
        <input type="hidden" name="modify" value="survivor" />
        <input type="hidden" name="asset_id" value="$survivor_id" />

        <div id="asset_management_left_pane">
            <input id="topline_name_fixed" class="full_width" type="text" name="name" value="$name" placeholder="Survivor Name"/>
            <br class="mobile_only"/><br class="mobile_only"/><br class="mobile_only"/>
            $epithets
            <br class="mobile_only"/>
            $add_epithets<br class="mobile_only"/>
            $rm_epithets
            <input onchange="this.form.submit()" class="full_width" type="text" name="add_epithet" placeholder="add a custom epithet"/>
            <hr class="mobile_only"/>

            <!-- SEX, SURVIVAL and MISC. SURVIVOR ATTRIBUTES -->

            <p>
             Survivor sex: <b>$sex</b>
            <div id="survivor_dead_retired_container">

                    <!-- favorite -->
                 <input type='hidden' value='unchecked' name='toggle_favorite'/>
                 <input type="checkbox" id="favorite" class="radio_principle" name="toggle_favorite" value="checked" $favorite_checked /> 
                 <label class="radio_principle_label toggle_favorite" for="favorite"> &#9733; Favorite </label>

                    <!-- dead -->
                 <input type='hidden' value='unchecked' name='toggle_dead'/>
                 <input type="checkbox" id="dead" class="radio_principle" name="toggle_dead" value="checked" onclick="showHide('COD')" $dead_checked /> 
                 <label class="radio_principle_label floating_label" for="dead"> Dead </label>

                    <!-- retired -->
                 <input type='hidden' value='unchecked' name='toggle_retired'/>
                 <input type="checkbox" id="retired" class="radio_principle" name="toggle_retired" value="checked" $retired_checked> 
                 <label class="radio_principle_label" for="retired" style="float: right; clear: none;"> Retired &nbsp; </label>
                </p>


                <div id="COD" style="display: $show_COD" >
                    <hr class="mobile_only"/> <img class="COD_down_arrow mobile_only" src="http://media.kdm-manager.com/icons/down_arrow.png"/>
                    <input onchange="this.form.submit()" class="full_width maroon" type="text" name="cause_of_death" placeholder="Cause of Death" value="$cause_of_death"/>
                </div>
            </div> <!-- survivor_dead_retired_container -->

            <hr class="mobile_only"/>

            <div id="survivor_survival_box_container">
                <div class="big_number_container left_margin">
                    <button class="incrementer mobile_only" onclick="increment('survivalBox');">+</button>
                    <input type="number" id="survivalBox" class="big_number_square" name="survival" value="$survival" max="$survival_limit" min="0"/>
                    <button class="decrementer mobile_only" onclick="decrement('survivalBox');">-</button>
                </div>
                <div class="big_number_caption">Survival <p>(max: $survival_limit)</p></div>
            </div> <!-- survivor_survival_box_container -->

            <hr class="mobile_only"/>

            <div id="survivor_survival_actions_container">
                <p>
                 <input type='hidden' value='unchecked' name='toggle_cannot_spend_survival'/>
                 <input onchange="this.form.submit()" type="checkbox" id="cannot_spend_survival" class="radio_principle" name="toggle_cannot_spend_survival" value="checked" $cannot_spend_survival_checked /> 
                 <label class="radio_principle_label" for="cannot_spend_survival"> Cannot spend survival </label>
                 $survival_actions
                </p>
            </div>

            <hr class="mobile_only"/>
            <div class="mobile_only">
                $fighting_arts
                $departure_buffs
                $abilities_and_impairments
                $disorders
            </div>

            <a id="edit_attribs" />

            <hr class="mobile_only"/> <!-- logical break; same form -->

            <div id="survivor_stats">
                <input id="movementBox" class="big_number_square" type="number" name="Movement" value="$movement"/>
                <div class="big_number_caption">Movement<br />
                    <div>
                    <button class="incrementer" onclick="increment('movementBox');">+</button>
                    <button class="decrementer" onclick="decrement('movementBox');">-</button>
                    </div>
                </div>
                <br class="mobile_only"/><hr/>
                <input id="accuracyBox" class="big_number_square" type="number" name="Accuracy" value="$accuracy"/>
                <div class="big_number_caption">Accuracy<br/>
                    <div>
                    <button class="incrementer" onclick="increment('accuracyBox');">+</button>
                    <button class="decrementer" onclick="decrement('accuracyBox');">-</button>
                    </div>
                </div>
                <br class="mobile_only"/><hr/>
                <input id="strengthBox" class="big_number_square" type="number" name="Strength" value="$strength"/>
                <div class="big_number_caption">Strength<br/>
                    <div>
                    <button class="incrementer" onclick="increment('strengthBox');">+</button>
                    <button class="decrementer" onclick="decrement('strengthBox');">-</button>
                    </div>
                </div>
                <br class="mobile_only"/><hr/>
                <input id="evasionBox" class="big_number_square" type="number" name="Evasion" value="$evasion"/>
                <div class="big_number_caption">Evasion<br/>
                    <div>
                    <button class="incrementer" onclick="increment('evasionBox');">+</button>
                    <button class="decrementer" onclick="decrement('evasionBox');">-</button>
                    </div>
                </div>
                <br class="mobile_only"/><hr/>
                <input id="luckBox" class="big_number_square" type="number" name="Luck" value="$luck"/>
                <div class="big_number_caption">Luck<br/>
                    <div>
                    <button class="incrementer" onclick="increment('luckBox');">+</button>
                    <button class="decrementer" onclick="decrement('luckBox');">-</button>
                    </div>
                </div>
                <br class="mobile_only"/><hr/>
                <input id="speedBox" class="big_number_square" type="number" name="Speed" value="$speed"/>
                <div class="big_number_caption">Speed<br/>
                    <div>
                    <button class="incrementer" onclick="increment('speedBox');">+</button>
                    <button class="decrementer" onclick="decrement('speedBox');">-</button>
                    </div>
                </div>
            </div> <!-- survivor_stats -->

            <br class="mobile_only"/>
            <hr/>


            <h3>Bonuses</h3>
            $settlement_buffs


            <a id="edit_hit_boxes" />

        </div> <!-- asset_management_left_pane -->

        <hr class="mobile_only"/>   <!-- LOGICAL/ORGANIZATIONAL break -->

        <div id="asset_management_middle_pane">
                        <!-- HIT BOXES ; still the same form -->
            <a> <!-- hacks!!! for inc/dec buttons-->
            <div id="survivor_hit_box">
                <div class="big_number_container right_border">
                    <button class="incrementer" onclick="increment('insanityBox');">+</button>
                        <input id="insanityBox" type="number" class="shield" name="Insanity" value="$insanity" style="color: $insanity_number_style;" min="0"/>
                        <font id="hit_box_insanity">Insanity</font>
                    <button class="decrementer" onclick="decrement('insanityBox');">-</button>
                </div>

                <div class="hit_box_detail">
                 <input type='hidden' value='unchecked' name='toggle_brain_damage_light'/>
                 <input type="checkbox" id="brain_damage_light" class="radio_principle" name="toggle_brain_damage_light" $brain_damage_light_checked /> 
                 <label id="damage_box" class="radio_principle_label" for="brain_damage_light"> L </label>
                    <h2>Brain</h2>
                    If your insanity is 3+, you are <b>Insane</b>.
                </div>
            </div> <!-- survivor_hit_box -->

                <!-- HEAD -->
            <div id="survivor_hit_box">
                <div class="big_number_container right_border">
                    <button class="incrementer" onclick="increment('headBox');">+</button>
                        <input id="headBox" type="number" class="shield" name="Head" value="$head" min="0"/>
                    <button class="decrementer" onclick="decrement('headBox');">-</button>
                </div>
                <div class="hit_box_detail">
                 <input type='hidden' value='unchecked' name='toggle_head_damage_heavy'/>
                 <input type="checkbox" id="head_damage_heavy" class="radio_principle" name="toggle_head_damage_heavy" $head_damage_heavy_checked /> 
                 <label id="damage_box" class="radio_principle_label" for="head_damage_heavy"> H </label>
                    <h2>Head</h2>
                    <font color="#C60000">H</font>eavy Injury: Knocked Down
                </div>
            </div> <!-- survivor_hit_box -->

                <!-- ARMS -->
            <div id="survivor_hit_box">
                <div class="big_number_container right_border">
                    <button class="incrementer" onclick="increment('armsBox');">+</button>
                        <input id="armsBox" type="number" class="shield" name="Arms" value="$arms" min="0"/>
                    <button class="decrementer" onclick="decrement('armsBox');">-</button>
                </div>
                <div class="hit_box_detail">
                 <input type='hidden' value='unchecked' name='toggle_arms_damage_heavy'/>
                 <input type="checkbox" id="arms_damage_heavy" class="radio_principle" name="toggle_arms_damage_heavy" $arms_damage_heavy_checked /> 
                 <label id="damage_box" class="radio_principle_label" for="arms_damage_heavy"> H </label>
                 <input type='hidden' value='unchecked' name='toggle_arms_damage_light'/>
                 <input type="checkbox" id="arms_damage_light" class="radio_principle" name="toggle_arms_damage_light" $arms_damage_light_checked /> 
                 <label id="damage_box" class="radio_principle_label" for="arms_damage_light"> L </label>
                    <h2>Arms</h2>
                    <font color="#C60000">H</font>eavy Injury: Knocked Down
                </div>
            </div> <!-- survivor_hit_box -->

                <!-- BODY -->
            <div id="survivor_hit_box">
                <div class="big_number_container right_border">
                    <button class="incrementer" onclick="increment('bodyBox');">+</button>
                        <input id="bodyBox" type="number" class="shield" name="Body" value="$body" min="0"/>
                    <button class="decrementer" onclick="decrement('bodyBox');">-</button>
                </div>
                <div class="hit_box_detail">
                 <input type='hidden' value='unchecked' name='toggle_body_damage_heavy'/>
                 <input type="checkbox" id="body_damage_heavy" class="radio_principle" name="toggle_body_damage_heavy" $body_damage_heavy_checked /> 
                 <label id="damage_box" class="radio_principle_label" for="body_damage_heavy"> H </label>
                 <input type='hidden' value='unchecked' name='toggle_body_damage_light'/>
                 <input type="checkbox" id="body_damage_light" class="radio_principle" name="toggle_body_damage_light" $body_damage_light_checked /> 
                 <label id="damage_box" class="radio_principle_label" for="body_damage_light"> L </label>
                    <h2>Body</h2>
                    <font color="#C60000">H</font>eavy Injury: Knocked Down
                </div>
            </div> <!-- survivor_hit_box -->

                <!-- WAIST -->
            <div id="survivor_hit_box">
                <div class="big_number_container right_border">
                    <button class="incrementer" onclick="increment('waistBox');">+</button>
                        <input id="waistBox" type="number" class="shield" name="Waist" value="$waist" min="0"/>
                    <button class="decrementer" onclick="decrement('waistBox');">-</button>
                </div>
                <div class="hit_box_detail">
                 <input type='hidden' value='unchecked' name='toggle_waist_damage_heavy'/>
                 <input type="checkbox" id="waist_damage_heavy" class="radio_principle" name="toggle_waist_damage_heavy" $waist_damage_heavy_checked /> 
                 <label id="damage_box" class="radio_principle_label" for="waist_damage_heavy"> H </label>
                 <input type='hidden' value='unchecked' name='toggle_waist_damage_light'/>
                 <input type="checkbox" id="waist_damage_light" class="radio_principle" name="toggle_waist_damage_light" $waist_damage_light_checked /> 
                 <label id="damage_box" class="radio_principle_label" for="waist_damage_light"> L </label>
                    <h2>Waist</h2>
                    <font color="#C60000">H</font>eavy Injury: Knocked Down
                </div>
            </div> <!-- survivor_hit_box -->

        <!-- LEGS -->
            <div id="survivor_hit_box">
                <div class="big_number_container right_border">
                    <button class="incrementer" onclick="increment('legsBox');">+</button>
                        <input id="legsBox" type="number" class="shield" name="Legs" value="$legs" min="0"/>
                    <button class="decrementer" onclick="decrement('legsBox');">-</button>
                </div>
                <div class="hit_box_detail">
                 <input type='hidden' value='unchecked' name='toggle_legs_damage_heavy'/>
                 <input type="checkbox" id="legs_damage_heavy" class="radio_principle" name="toggle_legs_damage_heavy" $legs_damage_heavy_checked /> 
                 <label id="damage_box" class="radio_principle_label" for="legs_damage_heavy"> H </label>
                 <input type='hidden' value='unchecked' name='toggle_legs_damage_light'/>
                 <input type="checkbox" id="legs_damage_light" class="radio_principle" name="toggle_legs_damage_light" $legs_damage_light_checked /> 
                 <label id="damage_box" class="radio_principle_label" for="legs_damage_light"> L </label>
                    <h2>Legs</h2>
                    <font color="#C60000">H</font>eavy Injury: Knocked Down
                </div>
            </div> <!-- survivor_hit_box -->


                <!-- HIT BOXES END HERE -->


                <!-- HEAL SURVIVOR CONTROLS HERE! -->

             <select name="heal_survivor" onchange="this.form.submit()">
              <option selected disabled hidden value="">Heal Survivor</option>
              <option>Heal Injuries Only</option>
              <option>Heal Injuries and Remove Armor</option>
              <option>Return from Hunt</option>
             </select>


            <hr/>  <!-- logical break -->


                        <!-- HUNT XP and AGE -->
            <div class="big_number_container left_margin">
                <button class="incrementer" onclick="increment('huntXpBox');">+</button>
                <input id="huntXpBox" class="big_number_square" type="number" name="hunt_xp" value="$hunt_xp" min="0"/>
                <button class="decrementer" onclick="decrement('huntXpBox');">-</button>
            </div>
            <div class="big_number_caption">Hunt XP</div>
            <br class="mobile_only"/>
            <p><img class="icon" src="$MEDIA_URL/icons/trigger_story_event.png" /> <b>Age</b> occurs at 2, 6, 10 and 15. The Survivor retires at 16.</p>

            <hr/>

                        <!-- WEAPON PROFICIENCY -->
            <div class="big_number_container left_margin">
                <button class="incrementer" onclick="increment('proficiencyBox');">+</button>
                <input onchange="this.form.submit()" id="proficiencyBox" class="big_number_square" type="number" name="Weapon Proficiency" value="$weapon_proficiency" min="0"/>
                <button class="decrementer" onclick="decrement('proficiencyBox');">-</button>
            </div>
            <div class="big_number_caption">Weapon Proficiency
                <input onchange="this.form.submit()" type="text" class="full_width" placeholder="Type: Select before hunt" value="$weapon_proficiency_type" name="weapon_proficiency_type" style="width: 50%; clear: none; "/>
            </div>
            <div class="desktop_indent">
                <p><b>Specialist</b> at 3<br/><b>Master</b> at 8</p>
            </div>

            <hr/>

                        <!-- COURAGE AND UNDERSTANDING -->

            <div class="big_number_container left_margin">
                <button class="incrementer" onclick="increment('courageBox');">+</button>
                <input id="courageBox" class="big_number_square" type="number" name="Courage" value="$courage" min="0"/>
                <button class="decrementer" onclick="decrement('courageBox');">-</button>
            </div>
            <div class="big_number_caption">Courage</div>
            <br class="mobile_only"/>
            <p>
              <img class="icon" src="$MEDIA_URL/icons/trigger_story_event.png" /> <b>Bold</b> (p. 107) occurs at 3<br/><img class="icon" src="$MEDIA_URL/icons/trigger_story_event.png" /> <b>See the Truth</b> (p.155) occurs at 9.
            </p>

            <hr/>

            <div class="big_number_container left_margin">
                <button class="incrementer" onclick="increment('understandingBox');">+</button>
                <input id="understandingBox" class="big_number_square" type="number" name="Understanding" value="$understanding" min="0"/>
                <button class="decrementer" onclick="decrement('understandingBox');">-</button>
            </div>
            <div class="big_number_caption">Understanding</div>
            <br class="mobile_only"/>
            <p>
               <img class="icon" src="$MEDIA_URL/icons/trigger_story_event.png" /> <b>Insight</b> (p.123) occurs at 3<br/><img class="icon" src="$MEDIA_URL/icons/trigger_story_event.png" /> <b>White Secret</b> (p.169) occurs at 9.
            </p>

            </form>


            <a id="edit_fighting_arts" class="mobile_only"> </a>


            <hr class="mobile_only"/> <!-- logical division; new form starts here too -->
        </div> <!-- asset_management_middle_pane -->




                        <!-- FIGHTING ARTS -->
        <div id="asset_management_right_pane"> <!-- asset_management_right_pane -->

            <form method="POST" id="autoForm" action="#edit_fighting_arts">
                <input type="hidden" name="form_id" value="survivor_edit_fighting_arts" />
                <button class="hidden"></button>
                <input type="hidden" name="modify" value="survivor" />
                <input type="hidden" name="asset_id" value="$survivor_id" />

                <h3>Fighting Arts</h3>
                 <input type='hidden' value='unchecked' name='toggle_cannot_use_fighting_arts'/>
                 <input onchange="this.form.submit()" type="checkbox" id="cannot_use_fighting_arts" class="radio_principle" name="toggle_cannot_use_fighting_arts" value="checked" $cannot_use_fighting_arts_checked />
                 <label class="radio_principle_label" for="cannot_use_fighting_arts" id="float_right_toggle"> Cannot use<br/>Fighting Arts </label>
                <p>Maximum 3.</p>

                    $fighting_arts
                    $add_fighting_arts<br class="mobile_only"/>
                    $rm_fighting_arts

            <a id="edit_disorders" class="mobile_only"></a>
            <hr class="mobile_only"/>

            </form>

                        <!-- DISORDERS - HAS ITS OWN FORM-->

            <form method="POST" id="autoForm" action="#edit_disorders">
                <input type="hidden" name="form_id" value="survivor_edit_disorders" />
                <input type="hidden" name="modify" value="survivor" />
                <input type="hidden" name="asset_id" value="$survivor_id" />
                <h3>Disorders</h3>
                <p>Maximum 3.</p>

                $disorders
                $add_disorders<br class="mobile_only"/>
                $rm_disorders

                <a id="edit_abilities" class="mobile_only"></a>

            </form>


            <hr class="mobile_only"/>

                        <!-- ABILITIES AND IMPAIRMENTS -->


            <h3>Abilities & Impairments</h3>
                <form method="POST" id="autoForm" action="#edit_abilities">
                  <input type="hidden" name="form_id" value="survivor_edit_abilities" />
                  <input type="hidden" name="modify" value="survivor" />
                  <input type="hidden" name="asset_id" value="$survivor_id" />
                  <input type='hidden' value='unchecked' name='toggle_skip_next_hunt'/>
                  <input onchange="this.form.submit()" type="checkbox" id="skip_next_hunt" class="radio_principle" name="toggle_skip_next_hunt" value="checked" $skip_next_hunt_checked />
                  <label class="radio_principle_label" for="skip_next_hunt" id="float_right_toggle"> Skip Next<br/>Hunt </label>
                </form>
            <p>
                <form method="POST" id="autoForm" action="#edit_abilities">
                  <input type="hidden" name="form_id" value="survivor_edit_abilities" />
                  <input type="hidden" name="modify" value="survivor" />
                  <input type="hidden" name="asset_id" value="$survivor_id" />
                    $abilities_and_impairments<br class="mobile_only"/>
                    $add_abilities_and_impairments
                <input onchange="this.form.submit()" class="full_width" type="text" name="add_ability" placeholder="add custom ability or impairment"/>
                    $remove_abilities_and_impairments
                </form>
            </p>

            <hr />

            <form method="POST" id="autoForm" action="#edit_abilities">
              <input type="hidden" name="form_id" value="survivor_edit_abilities"/>
              <input type="hidden" name="modify" value="survivor" />
              <input type="hidden" name="asset_id" value="$survivor_id" />
              <input onchange="this.form.submit()" class="full_width" type="text" name="email" placeholder="email" value="$email"/>
              <hr />
            </form>


            <br class="mobile_only"/><hr class="mobile_only"/>


            <form method="POST" onsubmit="return confirm('This cannot be undone! Press OK to permanently delete this survivor forever, which is NOT THE SAME THING as marking it dead: permanently deleting the survivor prevents anyone from viewing and/or editing it ever again! If you are trying to delete all survivors in a settlement, you may delete the settlement from the settlement editing view.');"><input type="hidden" name="remove_survivor" value="$survivor_id"/><button class="error">Permanently Delete Survivor</button></form>
            <hr class="mobile_only"/>
            <br class="mobile_only"/>
        </div> <!-- asset_management_right_pane -->
    \n""")


class settlement:
    new = """\n\
    <span class="desktop_only nav_bar gradient_green"></span>
    <br class="desktop_only"/>
    <div id="create_new_asset_form_container">
        <h3>Create a New Settlement!</h3>
        <form method="POST">
        <input type="hidden" name="new" value="settlement" />
        <input type="text" name="settlement_name" placeholder="Settlement Name"/ class="full_width" autofocus>
        <button class="success">SAVE</button>
        </form>
    </div>
    \n"""
    return_hunting_party = Template("""\n\
        <form method="POST">
            <input type="hidden" name="return_hunting_party" value="$settlement_id"/>
            <button id="return_hunting_party" class="bold gradient_orange" >&#8629; Return Hunting Party</button>
        </form>
    \n""")
    hunting_party_macros = Template("""\n\
    <h3>Update Hunting Party Stats:</h3>
    <div id="hunting_party_macro_container">
    <div class="hunting_party_macro" style="border-left: 0 none;">
        <form method="POST">
            <input type="hidden" name="modify" value="settlement"/>
            <input type="hidden" name="asset_id" value="$settlement_id"/>
            <input type="hidden" name="hunting_party_operation" value="survival"/>
            Survival
            <button name="operation" value="increment">+1</button>
            <button name="operation" value="decrement">-1</button>
        </form>
    </div>
    <div class="hunting_party_macro">
        <form method="POST">
            <input type="hidden" name="modify" value="settlement"/>
            <input type="hidden" name="asset_id" value="$settlement_id"/>
            <input type="hidden" name="hunting_party_operation" value="Insanity"/>
            Insanity
            <button name="operation" value="increment">+1</button>
            <button name="operation" value="decrement">-1</button>
        </form>
    </div>
    <div class="hunting_party_macro">
        <form method="POST">
            <input type="hidden" name="modify" value="settlement"/>
            <input type="hidden" name="asset_id" value="$settlement_id"/>
            <input type="hidden" name="hunting_party_operation" value="Courage"/>
            Courage
            <button name="operation" value="increment">+1</button>
            <button name="operation" value="decrement">-1</button>
        </form>
    </div>
    <div class="hunting_party_macro">
        <form method="POST">
            <input type="hidden" name="modify" value="settlement"/>
            <input type="hidden" name="asset_id" value="$settlement_id"/>
            <input type="hidden" name="hunting_party_operation" value="Understanding"/>
            Understanding
            <button name="operation" value="increment">+1</button>
            <button name="operation" value="decrement">-1</button>
        </form>
    </div>
    </div><!-- hunting party macro container -->

    <hr/>
    \n""")
    storage_warning = Template(""" onclick="return confirm('Remove $item_name from Settlement Storage?');" """)
    storage_remove_button = Template("""\n\
    \t<button $confirmation id="remove_item" name="remove_item" value="$item_key" style="background-color: #$item_color; color: #000;"> $item_key_and_count </button>
    \n""")
    storage_tag = Template('<h3 class="inventory_tag" style="color: #$color">$name</h3><hr/>')
    storage_resource_pool = Template("""\n\
    <p>Hide: $hide, Bone: $bone, Scrap: $scrap, Organ: $organ</p>
    <hr/>
    \n""")

    #   campaign view campaign summary
    campaign_summary_survivors_top = '<div id="campaign_summary_survivors">\n<h3 class="mobile_only">Survivors</h3>'
    campaign_summary_survivors_bot = '</div><hr class="mobile_only"/>'
    summary = Template("""\n\
        <span class="desktop_only nav_bar gradient_purple"></span>
        <h1 class="settlement_name"> %s $settlement_name</h1>
        <div id="campaign_summary_pop">
            <p>Population: $population ($sex_count); $death_count deaths</p>
            <hr class="mobile_only"/>
            <p>Survival Limit: $survival_limit</p>
            <hr class="mobile_only"/>
        </div>
        <form method="POST" class="mobile_only">
          <input type="hidden" name="change_view" value="new_survivor"/>
          <button class="success" id="campaign_summary_new_survivor">+ Create New Survivor</button>
          <hr/>
        </form>
        <a id="edit_hunting_party" class="mobile_only"></a>
        <span class="vertical_spacer desktop_only"></span>
            $survivors
        <div id="campaign_summary_facts_box">
            <form method="POST">
            <input type="hidden" name="change_view" value="new_survivor"/>
            <button class="success desktop_only" id="campaign_summary_new_survivor">+ Create New Survivor</button>
            </form>
            <div class="campaign_summary_small_box">
                <h3>Principles</h3>
                $principles
            </div>
            <div class="campaign_summary_small_box">
                <h3>Innovations</h3>
                $innovations
            </div>
            <hr class="mobile_only"/>
            <div class="campaign_summary_small_box">
                <h3>Bonuses</h3>
                <h4>Departing</h4>
                $departure_bonuses
                <h4>During Settlement</h4>
                $settlement_bonuses
                $survivor_bonuses
            </div>
            <hr class="mobile_only"/>
            <div class="campaign_summary_small_box">
                <h3>Locations</h3>
                <p>$locations</p>
            </div>
            <hr class="mobile_only"/>
            <div class="campaign_summary_small_box">
                <h3>Monsters</h3>
                <h4>Defeated</h4>
                <p>$defeated_monsters</p>
                <h4>Quarries</h4>
                <p>$quarries</p>
                <h4>Nemeses</h4>
                <p>$nemesis_monsters</p>
            </div>
        </div>
    \n""" % dashboard.campaign_flash)
    form = Template("""\n\
    $game_link

    <span class="desktop_only nav_bar gradient_orange"></span>
    <br class="desktop_only"/>

    <div id="asset_management_left_pane">
        <form method="POST" id="autoForm" action="#">
            <button id="save_button" class="success">Save</button>
            <input type="hidden" name="modify" value="settlement" />
            <input type="hidden" name="asset_id" value="$settlement_id" />

            <input id="topline_name" onchange="this.form.submit()" class="full_width" type="text" name="name" value="$name" placeholder="Settlement Name"/>
            <hr class="mobile_only"/>
            <div class="settlement_form_wide_box">
                <div class="big_number_container left_margin">
                    <button class="incrementer" onclick="increment('survivalLimitBox');">+</button>
                    <input id="survivalLimitBox" class="big_number_square" type="number" name="survival_limit" value="$survival_limit" min="$min_survival_limit"/>
                    <button class="decrementer" onclick="decrement('survivalLimitBox');">-</button>
                </div>
                <div class="big_number_caption ">Survival Limit<br />(min: $min_survival_limit)</div>
            </div>
            <br class="mobile_only"/>
            <hr class="mobile_only"/>

            <div class="settlement_form_wide_box">
                <div class="big_number_container left_margin">
                    <button class="incrementer" onclick="increment('populationBox');">+</button>
                    <input id="populationBox" class="big_number_square" type="number" name="population" value="$population" min="0"/>
                    <button class="decrementer" onclick="decrement('populationBox');">-</button>
                </div>
                <div class="big_number_caption">Population</div>
            </div> <!-- settlement_form_wide_box -->

            <br class="mobile_only"/><hr class="mobile_only"/>

            <div class="settlement_form_wide_box">
                <div class="big_number_container left_margin">
                    <button class="incrementer" onclick="increment('deathCountBox');">+</button>
                    <input id="deathCountBox" class="big_number_square" type="number" name="death_count" value="$death_count" min="0"/>
                    <button class="decrementer" onclick="decrement('deathCountBox');">-</button>
                </div>
                <div class="big_number_caption">Death Count</div>
            </div> <!-- settlement_form_wide_box -->

            <hr />

            <h3 class="mobile_only">On Departure</h3>
            $departure_bonuses

            <hr class="mobile_only"/>

            <h3 class="mobile_only">During Settlement Phase</h3>
            $settlement_bonuses

            <hr/>

            <br class="mobile_only"/>

        </form> <!-- ending the first form -->



                    <!-- STORAGE - THIS IS ITS OWN FORM-->
        <form id="autoForm" method="POST" action="#edit_storage">
            <input type="hidden" name="modify" value="settlement" />
            <input type="hidden" name="asset_id" value="$settlement_id" />
            <button id="remove_item" class="hidden" style="display: none" name="remove_item" value="" /> </button>
            <div id="block_group">
            <h2>Storage</h2>
            <p>Gear and Resources may be stored without limit. Tap an item to remove it once.</p>
            <hr />

        <a id="edit_storage" class="mobile_only"/></a>

            $storage
            $items_options<br />
             <input onchange="this.form.submit()" type="text" class="full_width" name="add_item" placeholder="add gear or resource"/>
            </div>
        </form>

    </div>
    <div id="asset_management_middle_pane">

                    <!-- LOCATIONS - THIS HAS ITS OWN FORM  -->

        <a id="edit_locations" class="mobile_only"><a/>
        <form id="autoForm" method="POST" action="#edit_locations">
        <input type="hidden" name="modify" value="settlement" />
        <input type="hidden" name="asset_id" value="$settlement_id" />

        <div id="block_group">
         <h2>Settlement Locations</h2>
         <p>Locations in your settlement.</p>
         $locations
         $locations_add
         $locations_rm
        </div>
        </form>

        <hr class="mobile_only"/>  <!-- Logical Section Break -->

                    <!-- INNOVATIONS - HAS ITS OWN FORM-->

        <a id="edit_innovations" class="mobile_only"/></a>
        <form id="autoForm" method="POST" action="#edit_innovations">
        <input type="hidden" name="modify" value="settlement" />
        <input type="hidden" name="asset_id" value="$settlement_id" />
        <div id="block_group">
         <h2>Innovations</h2>
         <p>The settlement's innovations (including weapon masteries).</p>
         $innovations
         $innovations_add
         $innovations_rm
         $innovation_deck
        </div>
        </form>

                    <!-- PRINCIPLES - HAS ITS OWN FORM-->

        <a id="edit_principles" class="mobile_only"></a>
        <form id="autoForm" method="POST" action="#edit_principles">
        <input type="hidden" name="modify" value="settlement" />
        <input type="hidden" name="asset_id" value="$settlement_id" />
        <div id="block_group">
         <h2>Principles</h2>
         <p>The settlement's established principles.</p>

            <div class="$new_life_principle_hidden">
            <h3>New Life Principle</h3>
             <fieldset class="settlement_principle">
              <input onchange="this.form.submit()" type="radio" id="protect_button" class="radio_principle" name="new_life_principle" value="Protect the Young" $protect_the_young_checked /> 
                <label class="radio_principle_label" for="protect_button"> Protect the Young </label>
              <input onchange="this.form.submit()" type="radio" id="survival_button" class="radio_principle" name="new_life_principle" value="Survival of the Fittest" $survival_of_the_fittest_checked /> 
                <label class="radio_principle_label" for="survival_button"> Survival of the fittest </label>
            </fieldset>
            </div>

            <div class="$death_principle_hidden">
             <h3>Death Principle</h3>
             <fieldset class="settlement_principle">
              <input onchange="this.form.submit()" type="radio" id="cannibalize_button" class="radio_principle" name="death_principle" value="Cannibalize" $cannibalize_checked /> 
                <label class="radio_principle_label" for="cannibalize_button"> Cannibalize </label>
              <input onchange="this.form.submit()" type="radio" id="graves_button" class="radio_principle" name="death_principle" value="Graves" $graves_checked /> 
                <label class="radio_principle_label" for="graves_button"> Graves </label>
             </fieldset>
            </div>

            <div class="$society_principle_hidden">
             <h3>Society Principle</h3>
             <fieldset class="settlement_principle">
              <input onchange="this.form.submit()" type="radio" id="collective_toil_button" class="radio_principle" name="society_principle" value="Collective Toil" $collective_toil_checked /> 
                <label class="radio_principle_label" for="collective_toil_button"> Collective Toil </label>
              <input onchange="this.form.submit()" type="radio" id="accept_darkness_button" class="radio_principle" name="society_principle" value="Accept Darkness" $accept_darkness_checked /> 
                <label class="radio_principle_label" for="accept_darkness_button"> Accept Darkness </label>
             </fieldset>
            </div>

            <div class="$conviction_principle_hidden">
             <h3>Conviction Principle</h3>
             <fieldset class="settlement_principle">
              <input onchange="this.form.submit()" type="radio" id="barbaric_button" class="radio_principle" name="conviction_principle" value="Barbaric" $barbaric_checked /> 
                <label class="radio_principle_label" for="barbaric_button"> Barbaric </label>
              <input onchange="this.form.submit()" type="radio" id="romantic_button" class="radio_principle" name="conviction_principle" value="Romantic" $romantic_checked /> 
                <label class="radio_principle_label" for="romantic_button"> Romantic </label>
             </fieldset>
            </div>

        $principles_rm

        </div> <!-- principle block group -->
        </form>

        <hr class="mobile_only"/>  <!-- Logical Section Break -->



                       <!-- MILESTONES - HAS ITS OWN FORM-->

        <a id="edit_milestones"/>
        <form id="autoForm" method="POST" action="#edit_milestones">
        <input type="hidden" name="modify" value="settlement" />
        <input type="hidden" name="asset_id" value="$settlement_id" />
        <div id="block_group">
         <h2>Milestone Story Events</h2>
         <p>Trigger these story events when milestone condition is met.</p>
    
            <hr />
            <input onchange="this.form.submit()" id="first_child" type="checkbox" name="First child is born" class="radio_principle" $first_child_checked></input>
            <label for="first_child" class="radio_principle_label">First child is born</label>
            <p> &ensp; <img class="icon" src="$MEDIA_URL/icons/trigger_story_event.png" /> <b>Principle: New Life</b> (p.145) </p>
            <hr />
            <input onchange="this.form.submit()" id="first_death" type="checkbox" name="First time death count is updated" class="radio_principle" $first_death_checked></input>
            <label for="first_death" class="radio_principle_label">First time death count is updated</label>
            <p> &ensp; <img class="icon" src="$MEDIA_URL/icons/trigger_story_event.png" /> <b>Principle: Death</b> (p.143) </p>
            <hr />
            <input onchange="this.form.submit()" id="pop_15" type="checkbox" name="Population reaches 15" class="radio_principle" $pop_15_checked></input>
            <label for="pop_15" class="radio_principle_label">Population reaches 15</label>
            <p> &ensp; <img class="icon" src="$MEDIA_URL/icons/trigger_story_event.png" /> <b>Principle: Society</b> (p.147) </p>
            <hr />
            <input onchange="this.form.submit()" id="5_innovations" type="checkbox" name="Settlement has 5 innovations" class="radio_principle" $five_innovations_checked></input>
            <label for="5_innovations" class="radio_principle_label">Settlement has 5 innovations</label>
            <p> &ensp; <img class="icon" src="$MEDIA_URL/icons/trigger_story_event.png" /> <b>Hooded Knight</b> (p.121) </p>
            <hr />
            <input onchange="this.form.submit()" id="game_over" type="checkbox" name="Population reaches 0" class="radio_principle" $game_over_checked></input>
            <label for="game_over" class="radio_principle_label">Population reaches 0</label>
            <p> &ensp; <img class="icon" src="$MEDIA_URL/icons/trigger_story_event.png" /> <b>Game Over</b> (p.179) </p>

        </div>
        </form>


        <hr class="mobile_only"/> <!-- Logical Section Break Here -->


                    <!-- QUARRIES - HAS ITS OWN FORM-->

        <a id="edit_quarries"/>
        <form id="autoForm" method="POST" action="#edit_quarries">
        <input type="hidden" name="modify" value="settlement" />
        <input type="hidden" name="asset_id" value="$settlement_id" />

        <div id="block_group">
         <h2>Quarries</h2>
         <p>The monsters your settlement can select to hunt.</p>
        <hr />
         <p>$quarries</p>
            $quarry_options
         <input onchange="this.form.submit()" type="text" class="full_width" name="add_quarry" placeholder="add custom quarry"/>
        </div>

        </form>

                    <!-- NEMESIS MONSTERS -->
        <a id="edit_nemeses"/>
        <form id="autoForm" method="POST" action="#edit_nemeses">
        <input type="hidden" name="modify" value="settlement" />
        <input type="hidden" name="asset_id" value="$settlement_id" />

        <div id="block_group">
        <h2>Nemesis Monsters</h2>
        <p>The available nemesis encounter monsters.</p>
        <hr>
        $nemesis_monsters
        </div>
        </form>

                    <!-- DEFEATED MONSTERS: HAS ITS OWN FORM -->

        <a id="edit_defeated_monsters"/>
        <form id="autoForm" method="POST" action="#edit_defeated_monsters">
        <input type="hidden" name="modify" value="settlement" />
        <input type="hidden" name="asset_id" value="$settlement_id" />

        <div id="block_group">
         <h2>Defeated Monsters</h2>
         <p>A list of defeated monsters and their level.</p>
         $defeated_monsters
         $defeated_monsters_add
         <input onchange="this.form.submit()" type="text" class="full_width" name="add_defeated_monster" placeholder="add defeated monster"/>
        </div>
        </form>
    </div>


    <div id="asset_management_right_pane">

                    <!-- TIMELINE: HAS ITS OWN FORM  -->

        <a id="edit_timeline" class="mobile_only"></a>
        <form id="autoForm" method="POST" action="#edit_timeline">
        <input type="hidden" name="modify" value="settlement" />
        <input type="hidden" name="asset_id" value="$settlement_id" />

        <br class="mobile_only"/>
        <h2 class="clickable gradient_orange" onclick="showHide('timelineBlock')">LY $lantern_year - View Timeline <img class="dashboard_down_arrow" src="http://media.kdm-manager.com/icons/down_arrow.png"/> </h2>
        <div id="timelineBlock" class="block_group" style="display: none;">
         <div class="big_number_container left_margin">
             <button class="incrementer" onclick="increment('lanternYearBox');">+</button>
             <input id="lanternYearBox" onchange="this.form.submit()" class="big_number_square" type="number" name="lantern_year" value="$lantern_year" min="1"/>
             <button class="decrementer" onclick="decrement('lanternYearBox');">-</button>
         </div>
         <div class="big_number_caption">Lantern Year</div>
         <br class="mobile_only"/><hr class="mobile_only"/>
         $timeline
        </div> <!-- timelineBlock -->
        </form>


        <br class="mobile_only"/>

                    <!-- LOST SETTLEMENTS HAS ITS OWN FORM-->
        <div class="block_group">
            <a id="edit_lost_settlements" class="mobile_only"></a>
            <form id="autoForm" method="POST" action="#edit_lost_settlements">
            <input type="hidden" name="modify" value="settlement" />
            <input type="hidden" name="asset_id" value="$settlement_id" />

            <input onchange="this.form.submit()" class="big_number_square" type="number" name="lost_settlements" value="$lost_settlements"/>
            <h3>Lost Settlements</h3>
            <p>Refer to <img class="icon" src="$MEDIA_URL/icons/trigger_story_event.png" /> <b>Game Over</b> on p.179;  <img class="icon" src="$MEDIA_URL/icons/trigger_story_event.png" /> <b>Left Overs</b> occurs at 4;  <img class="icon" src="$MEDIA_URL/icons/trigger_story_event.png" /> <b>Those Before Us</b> occurs at 8; <img class="icon" src="$MEDIA_URL/icons/trigger_story_event.png" /> <b>Ocular Parasites</b> occurs at 12; <img class="icon" src="$MEDIA_URL/icons/trigger_story_event.png" /> <b>Rainy Season</b> occurs at 16.</p>
            </form>
        </div>
        <br />

        $survivors

        <br class="mobile_only"/>
        <hr class="mobile_only"/>

        <form method="POST">
        <input type="hidden" name="change_view" value="new_survivor"/>
        <button class="success">+ Create New Survivor</button>
        </form>

        <hr/>

    <form method="POST" onsubmit="return confirm('This cannot be undone! Press OK to permanently delete this settlement AND ALL SURVIVORS WHO BELONG TO THIS SETTLEMENT forever.');"><input type="hidden" name="remove_settlement" value="$settlement_id"/><button class="error">Permanently Delete Settlement</button></form>
    </div>
    \n""")



class login:
    """ The HTML for form-based authentication goes here."""
    form = """\n\
    <div id="sign_in_container">
        <h2 class="seo">KD:M Manager!</h2>
        <h1 class="seo">A campaign manager for <a href="http://kingdomdeath.com/" target="top">Kingdom Death</a> Monster.</h1>
        <div id="sign_in_controls">
            <form method="POST">
            <input class="sign_in" type="text" name="login" placeholder="email"/ autofocus>
            <input class="sign_in" type="password" name="password" placeholder="password"/>
            <button class="sign_in gradient_green">Sign In or Register</button>
            </form>
        </div>
    </div> <!-- sign_in_container -->
    \n"""
    new_user = Template("""\n\
    <div id="sign_in_container">
        <h2 class="seo">Create a New User!</h2>
        <h1 class="seo">Use an email address to share campaigns with friends.</h1>
        <div id="sign_in_controls">
            <form method="POST">
            <input class="sign_in" type="text" name="login" value="$login"/>
            <input class="sign_in" type="password" name="password" placeholder="password"/>
            <input class="sign_in" type="password" name="password_again" placeholder="password (again)"/>
            <button class="sign_in gradient_green">Register New User</button>
            </form>
        </div>
    </div> <!-- sign_in_container -->
    \n""")




class meta:
    """ This is for HTML that doesn't really fit anywhere else, in terms of
    views, etc. Use this for helpers/containers/administrivia/etc. """
    start_head = '<!DOCTYPE html>\n<html>\n<head>\n<meta charset="UTF-8">\n<title>%s</title>\n' % settings.get("application","title")
    stylesheet = Template('<link rel="stylesheet" type="text/css" href="$url">\n')
    false_body = 'Caught exception while rendering the current view!<hr/>The current session will be ended. Please try again.'
    close_body = '\n </div><!-- container -->\n</body>\n</html>'
    saved_dialog = '\n    <div id="saved_dialog" class="success">Saved!</div>'
    log_out_button = Template('\n\t<hr class="mobile_only"/><form id="logout" method="POST"><input type="hidden" name="remove_session" value="$session_id"/><input type="hidden" name="login" value="$login"/><button class="warn change_view mobile_only">SIGN OUT</button>\n\t</form>')
    mobile_hr = '<hr class="mobile_only"/>'
    dashboard_alert = Template("""\n\
    <br/><br/>
    <div class="dashboard_alert maroon">
    $msg
    </div>
    \n""")




#
#   application helper functions for HTML interfacing
#

def set_cookie_js(session_id):
    """ This returns a snippet of javascript that, if inserted into the html
    head will set the cookie to have the session_id given as the first/only
    argument to this function.

    Note that the cookie will not appear to have the correct session ID until
    the NEXT page load after the one where the cookie is set.    """
    expiration = datetime.now() + timedelta(days=1)
    cookie = Cookie.SimpleCookie()
    cookie["session"] = session_id
    cookie["session"]["expires"] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")
    return cookie.js_output()


def authenticate_by_form(params):
    """ Pass this a cgi.FieldStorage() to try to manually authenticate a user"""

    if "password_again" in params:
        if "login" in params and "password" in params:
            create_new = admin.create_new_user(params["login"].value.strip().lower(), params["password"].value.strip(), params["password_again"].value.strip())
            if create_new == False:
                output = user_error_msg.safe_substitute(err_class="warn", err_msg="Passwords did not match! Please re-enter.")
            elif create_new is None:
                output = user_error_msg.safe_substitute(err_class="warn", err_msg="Email address could not be verified! Please re-enter.")
            elif create_new == True:
                pass
            else:
                logger.exception("admin.create_new_user returned unexpected results!")
                logger.error(create_new)
    if "login" in params and "password" in params:
        auth = admin.authenticate(params["login"].value.strip().lower(), params["password"].value.strip())
        if auth == False:
            output = user_error_msg.safe_substitute(err_class="error", err_msg="Invalid password! Please re-enter.")
            output += login.form
        elif auth is None:
            output = login.new_user.safe_substitute(login=params["login"].value.strip().lower())
        elif auth == True:
            s = Session()
            session_id = s.new(params["login"].value.strip().lower())
            s.User.mark_usage("authenticated successfully")
            html, body = s.current_view_html()
            render(html, body_class=body, head=[set_cookie_js(session_id)])
    else:
        output = login.form
    return output



#
#   render() funcs are the only thing that goes below here.
#


def render(view_html, head=[], http_headers=None, body_class=None):
    """ This is our basic render: feed it HTML to change what gets rendered. """

    output = http_headers
    if http_headers is None:
        output = "Content-type: text/html\n\n"
    else:
        output = http_headers
        output += view_html
        print output
        sys.exit()

    output += meta.start_head
    output += meta.stylesheet.safe_substitute(url=settings.get("application", "stylesheet"))

    output += """\n\
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.js"></script>
    <script src="http://malsup.github.com/jquery.form.js"></script>

    <script>

        $(document).ready(function() {

            $('#saved_dialog').hide();

            $('#autoForm').ajaxForm(function() {
                $('#saved_dialog').show();
                $('#saved_dialog').fadeOut(1500)
            });

            $('.autoFormChild').ajaxForm(function() {
                 $('#saved_dialog').show();
                 $('#saved_dialog').fadeOut(1500)
            });

        });

    </script>
    \n"""

    output += """\n\
        <script>
        function increment(elem_id) {
            document.getElementById(elem_id).stepUp();
        }
        function decrement(elem_id) {
            document.getElementById(elem_id).stepDown();
        }
        </script>
        <script>
        function showHide(id) {
            var e = document.getElementById(id);
            if (e.style.display != 'none') e.style.display = 'none';
            else e.style.display = 'block';
        }
        </script>
    \n"""

    output += """\n\
    <script>
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
      })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

      ga('create', 'UA-71038485-1', 'auto');
      ga('send', 'pageview');

    </script>
    \n"""

    for element in head:
        output += element

    output += '</head>\n<body class="%s">\n <div id="container">\n' % body_class
    if view_html:
        output += view_html
    else:
        output += meta.false_body
    output += meta.close_body

    print(output)
    sys.exit(0)     # this seems redundant, but it's necessary in case we want
                    #   to call a render() in the middle of a load, e.g. to just
                    #   finish whatever we're doing and show a page.
