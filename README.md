<img width="1000" height="125" alt="Frame 1(7)" src="https://github.com/user-attachments/assets/fad3bc7a-67be-4be1-ad12-0e4b27ec5f6d" />

# The Secret Weapon Information

You've been tasked with building the secret weapon, your goal is simple: Help build the largest collaborative PCB alongside 100 other highschoolers!

**Try to read all of this before adding something to the board, it's important information!**

It's as simple as this:

* Put your name down for what schematic sheet you're working on (so we don't have merge conflicts)
* Fork/clone the repository
* Go into the schematic sheet you put yourself down for and rename it to your name + what you're working on!
* Wire up your component in the schematic (don't mess with other people's schematics without specific permission, unless they've added like an MCU or something), please don't add components that costs more than $5, so that we can get this thing made hopefully affordably!
* Route your component, make sure to have clean routing so that you don't take up too much space on the board! Also follow the routing guidelines that I listed in the PCB stackup information down below
* Commit the changes to your forked repository and open up a pull request!


I've added the root power system, it has 3 rails:

* 12V, 15A - Large components, high current/voltage, keep trace thick to high current stuff
* 5V, 4 - 5A - Medium currents, mid current/voltage, keep traces decently thick for mid current stuff
* 3V3. 1.5A - Low level systems, low current/voltage, don't use too much current on this layer


L3 is a 3V3 power fill, so you can just use a via to get down to it. If you need 5V or 12V, route it on the power layer, and then via up to use it!

The PCB stackup (how the layers are organized) is:

* TOP/SIGNAL  - Use this for routing!!! Put components on it too!
* GND - DON'T ROUTE ANYTHING ON THIS LAYER, if you need analog/split ground know what you're doing.
* PWR - Only route power stuff on this layer, and try to keep it clean
* SIGNAL - High speed routing if anyone wants, try to use the top and bottom and only use this if you need to
* GND - DON'T ROUTE ANYTHING ON THIS LAYER, if you need analog ground/split know what you're doing.
* BOTTOM/SIGNAL - Use this for routing!!! Don't put components on it though, but you're free to add silkscreen to it!


If any of your components need power or ground, you can just put a via down to either the ground or power layers. You can see how I did this with the TMC2209 driver I added in the very top left of the board!

Let's embrace the chaos, but try to make sure that whatever you're doing is actually wired/routed properly so we don't ruin the board for everyone else. When you make your PR, I might modify it a bit to work properly if I see something that's wrong, and it might also need to be re-routed if I'm behind on merging PR's! Also run DRC and check your part of the PCB, I'll also be fixing some of these if need be.

Try also not to add anything crazy big that takes up like a quarter for the board, or something that intentionally hoards power all the time, keep everyone else in mind with your components! Try to keep your components to like one big thing, and then you can add like decoupling, passives, etc. If there's no more I/O's left, you'll need to add an MCU, or wait for someone else to add one!

Try not to move other people's pins around on the MCU's, or mess with the root systems unless you know what you're doing, some people need specific peripherals!

If you need any help, or to verify anything, feel free to put it in this channel and someone will definitely help!

Also feel free to customize your schematic sheet by adding text, and also add some cool silkscreen or drawings underneath your components.

**PLEASE KEEP ALL COMPONENTS TO THE TOP LAYER**, we want to make our board easily manufacturable and there's very few things that need components on both sides.
