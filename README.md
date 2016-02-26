Cod4rotate Plugin for BigBrotherBot [![BigBrotherBot](http://i.imgur.com/7sljo4G.png)][B3]
=================================

Description
-----------

A [BigBrotherBot][B3] plugin that prevents your server from going stuck by automatically rotating the current map when 
no activity is detected on the server for a configurable amount of time.

Requirements
------------

* B3 1.10 (or higher version)

Download
--------

Latest version available [here](https://github.com/danielepantaleone/b3-plugin-cod4rotate/archive/master.zip).

Installation
------------

* copy the `cod4rotate` folder into `b3/extplugins`
* add to the `plugins` section of your `b3.xml` config file:

  ```xml
  <plugin name="cod4rotate" config="@b3/extplugins/cod4rotate/conf/plugin_cod4rotate.ini" />
  ```

Support
-------

If you have found a bug or have a suggestion for this plugin, please report it on the [B3 forums][Support].

[B3]: http://www.bigbrotherbot.net/ "BigBrotherBot (B3)"
[Support]: http://forum.bigbrotherbot.net/general-discussion/map_rotation-plugin-7189 "Support topic on the B3 forums"