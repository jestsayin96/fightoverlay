#!/usr/bin/env python3
"""Generate the Jester's Village setup & command guide PDF."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)

W, H = letter
TEAL = HexColor("#2de6c8")
DARK = HexColor("#060b0f")
GOLD = HexColor("#ffb224")
RED  = HexColor("#ff4d6d")
DIM  = HexColor("#8899aa")
WHITE = HexColor("#f0f4f8")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle("Title2", parent=styles["Title"], fontSize=22,
    textColor=TEAL, spaceAfter=6))
styles.add(ParagraphStyle("Sub", parent=styles["Normal"], fontSize=11,
    textColor=DIM, spaceAfter=14))
styles.add(ParagraphStyle("H1", parent=styles["Heading1"], fontSize=16,
    textColor=TEAL, spaceBefore=18, spaceAfter=8))
styles.add(ParagraphStyle("H2", parent=styles["Heading2"], fontSize=13,
    textColor=GOLD, spaceBefore=14, spaceAfter=6))
styles.add(ParagraphStyle("Body", parent=styles["Normal"], fontSize=10,
    leading=14, spaceAfter=6))
styles.add(ParagraphStyle("Cmd", parent=styles["Normal"], fontSize=10,
    leading=14, spaceAfter=2, fontName="Courier"))
styles.add(ParagraphStyle("Note", parent=styles["Normal"], fontSize=9,
    leading=12, textColor=DIM, leftIndent=18, spaceAfter=6))
styles.add(ParagraphStyle("Small", parent=styles["Normal"], fontSize=8,
    textColor=DIM))

doc = SimpleDocTemplate(
    "/home/claude/fightoverlay/Jesters_Village_Guide.pdf",
    pagesize=letter,
    leftMargin=0.75*inch, rightMargin=0.75*inch,
    topMargin=0.75*inch, bottomMargin=0.75*inch,
)

story = []

# ── TITLE ──
story.append(Paragraph("Jester's Village", styles["Title2"]))
story.append(Paragraph("Stream Overlay &mdash; Setup &amp; Command Guide", styles["Sub"]))
story.append(HRFlowable(width="100%", thickness=1, color=TEAL))
story.append(Spacer(1, 12))

# ── WHAT IS IT ──
story.append(Paragraph("What Is Jester's Village?", styles["H1"]))
story.append(Paragraph(
    "Jester's Village is a Twitch stream overlay where your chat becomes heroes "
    "who automatically fight monsters along the bottom of your stream. Viewers "
    "join just by chatting &mdash; no command needed. They earn loyalty points, "
    "buy gear, duel each other, and take on bosses together. Everything runs in "
    "a single browser source in OBS.", styles["Body"]))

# ── SETUP ──
story.append(Paragraph("Setup Instructions", styles["H1"]))

story.append(Paragraph("Step 1 &mdash; Create a Twitch Application", styles["H2"]))
story.append(Paragraph("1. Go to <b>dev.twitch.tv/console/apps</b> and log in.", styles["Body"]))
story.append(Paragraph("2. Click <b>Register Your Application</b>.", styles["Body"]))
story.append(Paragraph("3. Name: anything (e.g. \"Jester's Village\").", styles["Body"]))
story.append(Paragraph("4. OAuth Redirect URL: <b>https://jestsayin96.github.io/fightoverlay/</b>", styles["Body"]))
story.append(Paragraph("5. Category: <b>Chat Bot</b>.", styles["Body"]))
story.append(Paragraph("6. Client Type: <b>Confidential</b>.", styles["Body"]))
story.append(Paragraph("7. Click <b>Create</b>, then copy your <b>Client ID</b>.", styles["Body"]))

story.append(Paragraph("Step 2 &mdash; Authorize the Overlay", styles["H2"]))
story.append(Paragraph(
    "1. Open <b>https://jestsayin96.github.io/fightoverlay/?channel=YOURCHANNEL</b> "
    "in your browser (replace YOURCHANNEL with your Twitch username).", styles["Body"]))
story.append(Paragraph("2. Press <b>S</b> on your keyboard to open the setup panel.", styles["Body"]))
story.append(Paragraph("3. Paste your <b>Client ID</b> into the Client ID field.", styles["Body"]))
story.append(Paragraph("4. Click <b>AUTHORIZE ON TWITCH</b> and approve the permissions.", styles["Body"]))
story.append(Paragraph("5. You'll be redirected back. The status should say <b>Connected</b>.", styles["Body"]))
story.append(Paragraph("6. Click <b>COPY OBS URL</b> &mdash; this copies a URL with your token baked in.", styles["Body"]))

story.append(Paragraph("Step 3 &mdash; Add to OBS", styles["H2"]))
story.append(Paragraph("1. In OBS, click <b>+</b> under Sources &rarr; <b>Browser</b>.", styles["Body"]))
story.append(Paragraph("2. Name it \"Jester's Village\".", styles["Body"]))
story.append(Paragraph("3. Paste the URL you copied in Step 2.", styles["Body"]))
story.append(Paragraph("4. Set Width to <b>1920</b> and Height to <b>1080</b>.", styles["Body"]))
story.append(Paragraph("5. Uncheck \"Control audio via OBS\".", styles["Body"]))
story.append(Paragraph("6. Click <b>OK</b>. Heroes and monsters should appear along the bottom of your stream.", styles["Body"]))
story.append(Paragraph(
    "<i>Important: The OBS URL contains your token. Do not share it publicly. "
    "If you need to reset it, repeat Step 2.</i>", styles["Note"]))

story.append(Paragraph("Step 4 &mdash; Set Up Channel Point Rewards (Optional)", styles["H2"]))
story.append(Paragraph(
    "Channel point rewards let viewers spend points to summon bosses, monsters, "
    "and loot chests. Create these custom rewards on your Twitch dashboard:", styles["Body"]))

rewards_data = [
    ["Reward Name", "Cost", "What It Does", "Cooldown"],
    ["Summon the Boss", "1000+", "Spawns a boss for the village to fight", "Yes (5 min)"],
    ["Loot Chest / Treasure Drop", "300+", "Drops a loot chest", "No"],
    ["Spawn a Monster", "500+", "Spawns a tough monster", "No"],
]
t = Table(rewards_data, colWidths=[1.8*inch, 0.7*inch, 2.8*inch, 1.2*inch])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), TEAL),
    ("TEXTCOLOR", (0, 0), (-1, 0), DARK),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("GRID", (0, 0), (-1, -1), 0.5, DIM),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story.append(t)
story.append(Paragraph(
    "<i>The overlay matches rewards by keywords in the name: \"boss/raid/invade/titan\" "
    "triggers a boss, \"loot/chest/drop/treasure\" drops loot, \"monster/mob/goblin/horde/spawn\" "
    "spawns a monster. Unrecognized rewards are ignored.</i>", styles["Note"]))

# ── CACHE ──
story.append(Paragraph("Clearing OBS Cache", styles["H2"]))
story.append(Paragraph(
    "If OBS shows old behavior after an update, clear its browser cache:", styles["Body"]))
story.append(Paragraph("1. Close OBS completely.", styles["Body"]))
story.append(Paragraph("2. Open File Explorer, paste: <b>%APPDATA%\\obs-studio\\plugin_config\\obs-browser\\</b>", styles["Body"]))
story.append(Paragraph("3. Delete the <b>Cache</b> folder.", styles["Body"]))
story.append(Paragraph("4. Reopen OBS.", styles["Body"]))

story.append(PageBreak())

# ── COMMANDS ──
story.append(Paragraph("Chat Commands", styles["H1"]))
story.append(Paragraph(
    "Every Jester's Village command starts with <b>!v</b>. Viewers join the village "
    "just by chatting &mdash; no command needed.", styles["Body"]))

story.append(Paragraph("Emotes &amp; Actions (Everyone)", styles["H2"]))
cmds_emote = [
    ["Command", "What It Does"],
    ["!vjump", "Hero jumps"],
    ["!vdance", "Hero dances"],
    ["!vsit", "Hero sits down"],
    ["!vwave", "Hero waves"],
    ["!vhat", "Cycles through hat animation"],
    ["!vcharge", "Hero charges forward"],
    ["!vstats", "Hero strikes a stats pose"],
]
t = Table(cmds_emote, colWidths=[1.8*inch, 4.7*inch])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), TEAL),
    ("TEXTCOLOR", (0, 0), (-1, 0), DARK),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTNAME", (0, 1), (0, -1), "Courier"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("GRID", (0, 0), (-1, -1), 0.5, DIM),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
]))
story.append(t)
story.append(Spacer(1, 8))

story.append(Paragraph("Social &amp; Combat (Everyone)", styles["H2"]))
cmds_social = [
    ["Command", "What It Does"],
    ["!vhug name", "Walk over and hug another hero"],
    ["!vattack name", "Walk over and slap another hero (also !vslap, !vpunch)"],
    ["!vbomb", "Drop a bomb (hits nearby heroes and monsters)"],
    ["!vexplode", "Explode yourself (mods can explode others: !vexplode name)"],
    ["!vcolor red", "Change your hero's shirt color (any CSS color)"],
    ["!vrandom", "Randomize your hat, color, and class"],
]
t = Table(cmds_social, colWidths=[1.8*inch, 4.7*inch])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), TEAL),
    ("TEXTCOLOR", (0, 0), (-1, 0), DARK),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTNAME", (0, 1), (0, -1), "Courier"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("GRID", (0, 0), (-1, -1), 0.5, DIM),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
]))
story.append(t)
story.append(Spacer(1, 8))

story.append(Paragraph("Economy &amp; Shop (Everyone)", styles["H2"]))
cmds_econ = [
    ["Command", "What It Does"],
    ["!vpoints", "Check your loyalty points (also !vcoins, !vgold)"],
    ["!vshop", "See items and prices"],
    ["!vbuy crown", "Buy an item (hats: jester 20, cap 15, horns 25, halo 40, crown 60)"],
    ["!vbuy mage", "Buy a class (mage 35, cleric 35, rogue 30, barbarian 30, knight 30, paladin 45, ranger 40)"],
    ["!vavatar mage", "Switch to a class you own"],
    ["!vgive name 10", "Give loyalty points to another hero"],
    ["!vtop", "Show the top 5 leaderboard (also !vlb)"],
]
t = Table(cmds_econ, colWidths=[1.8*inch, 4.7*inch])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), GOLD),
    ("TEXTCOLOR", (0, 0), (-1, 0), DARK),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTNAME", (0, 1), (0, -1), "Courier"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("GRID", (0, 0), (-1, -1), 0.5, DIM),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
]))
story.append(t)
story.append(Spacer(1, 8))

story.append(Paragraph("Minigames (Everyone)", styles["H2"]))
cmds_mini = [
    ["Command", "What It Does"],
    ["!vduel name 10", "Challenge someone to a 1v1 duel with a point wager"],
    ["!vaccept", "Accept a duel challenge"],
    ["!vslots 10", "Play the slot machine (wager loyalty points)"],
    ["!vjoin", "Join a royale or a boss fight in progress"],
    ["!vshoot 5", "Shoot in basketball (pick a spot 1-9)"],
]
t = Table(cmds_mini, colWidths=[1.8*inch, 4.7*inch])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), GOLD),
    ("TEXTCOLOR", (0, 0), (-1, 0), DARK),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTNAME", (0, 1), (0, -1), "Courier"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("GRID", (0, 0), (-1, -1), 0.5, DIM),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
]))
story.append(t)
story.append(Spacer(1, 8))

story.append(Paragraph("Fun &amp; Info (Everyone)", styles["H2"]))
cmds_fun = [
    ["Command", "What It Does"],
    ["!vroll 2d6", "Roll dice (default: 1d20)"],
    ["!v8ball", "Ask the magic 8-ball"],
    ["!vlog", "Show the battle log for 15 seconds"],
    ["!vhelp", "Show all commands in the log (also !vcommands)"],
    ["!vhideavatar", "Hide your hero from the overlay (chat again to come back)"],
]
t = Table(cmds_fun, colWidths=[1.8*inch, 4.7*inch])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), TEAL),
    ("TEXTCOLOR", (0, 0), (-1, 0), DARK),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTNAME", (0, 1), (0, -1), "Courier"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("GRID", (0, 0), (-1, -1), 0.5, DIM),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
]))
story.append(t)
story.append(Spacer(1, 8))

story.append(Paragraph("Broadcaster &amp; Mod Only", styles["H2"]))
cmds_mod = [
    ["Command", "What It Does"],
    ["!vboss", "Summon a boss (viewers use channel points instead)"],
    ["!vmegaboss", "Summon the Mega Boss (30 levels above the top hero)"],
    ["!vroyale", "Start a battle royale (viewers type !vjoin to enter)"],
    ["!vbasketball", "Start a basketball minigame (viewers !vshoot 1-9)"],
    ["!vmass dance", "Make all heroes do an action (dance, jump, wave, hug, attack, bomb, explode)"],
    ["!vlounge", "Switch to lounge mode (no monsters, heroes hang out)"],
    ["!vwar", "Switch back to war mode (also !vfight, !vvillage)"],
]
t = Table(cmds_mod, colWidths=[1.8*inch, 4.7*inch])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), RED),
    ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTNAME", (0, 1), (0, -1), "Courier"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("GRID", (0, 0), (-1, -1), 0.5, DIM),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
]))
story.append(t)
story.append(Spacer(1, 8))

# ── KEYBOARD SHORTCUTS ──
story.append(Paragraph("Keyboard Shortcuts (Browser Only)", styles["H2"]))
story.append(Paragraph(
    "These work when viewing the overlay in a browser, not in OBS:", styles["Body"]))
cmds_keys = [
    ["Key", "What It Does"],
    ["S", "Open/close the setup panel"],
    ["V", "Toggle the battle log permanently"],
    ["D", "Start/stop demo mode (fake chatters)"],
]
t = Table(cmds_keys, colWidths=[1.8*inch, 4.7*inch])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), DIM),
    ("TEXTCOLOR", (0, 0), (-1, 0), DARK),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTNAME", (0, 1), (0, -1), "Courier"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("GRID", (0, 0), (-1, -1), 0.5, DIM),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
]))
story.append(t)

# ── NOTES ──
story.append(Spacer(1, 16))
story.append(HRFlowable(width="100%", thickness=1, color=DIM))
story.append(Spacer(1, 8))
story.append(Paragraph("Notes", styles["H1"]))
story.append(Paragraph(
    "<b>How viewers join:</b> Just chat. Any message in Twitch chat spawns a hero. "
    "No command needed.", styles["Body"]))
story.append(Paragraph(
    "<b>Loyalty points:</b> Earned passively by chatting (1 point per ~12 seconds of activity). "
    "Spent in the shop or wagered in duels and slots.", styles["Body"]))
story.append(Paragraph(
    "<b>Coexistence with Bellmire HD:</b> All village commands use the !v prefix "
    "to avoid conflicts. Bellmire's commands (!roll, !log, etc.) are unaffected.", styles["Body"]))
story.append(Paragraph(
    "<b>Token expiration:</b> Your OAuth token expires after ~60 days. "
    "If channel point rewards stop working, repeat Step 2 to get a fresh token "
    "and update the OBS URL.", styles["Body"]))
story.append(Paragraph(
    "<b>Multiple instances:</b> Only run the overlay in ONE place at a time "
    "(OBS only, not also in a browser tab). Two copies cause IRC conflicts.", styles["Body"]))

story.append(Spacer(1, 20))
story.append(Paragraph(
    "Jester's Village &copy; Jose Luis Estrada (JestSayin96). All rights reserved.",
    styles["Small"]))

doc.build(story)
print("PDF created: Jesters_Village_Guide.pdf")
