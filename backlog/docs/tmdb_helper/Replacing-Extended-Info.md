## Usage

TMDbHelper provides a simple window manager for tracking history between DialogVideoInfo. 

This function allows triggering a new info dialog to open when clicking another item inside the dialog (e.g. to open info for recommended movie or a cast member etc.). The window manager keeps a history of each info dialog opened this way. 

When the user closes the info dialog, the window manager move back one place in the history and reopen the info dialog for that item. This continues until the user reaches the original item, at which point closing the info dialog stops the window manager.

## Custom window

TMDbHelper requires a custom window which will act as the "base" window for the background behind the info dialog.

Any free custom window ID can be used (in the examples here I'm using 1190). The custom window should be empty other than for a required hidden list with id="9999", and, optionally, a background and busy indicator.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<window type="window" id="1190">
    <defaultcontrol always="true">9999</defaultcontrol>
    <controls>
        <!-- OPTIONAL: Code from your skin for window background e.g. 
        <include>Global_Background</include> 
        -->

        <!-- REQUIRED: TMDbHelper control list -->
        <control type="list" id="9999">
            <top>-1000</top>
            <left>-1000</left>
            <width>1</width>
            <height>1</height>
            <itemlayout />
            <focusedlayout />
            <content target="videos">$INFO[Window(Home).Property(TMDbHelper.Path.Current)]</content>
        </control>

        <!-- OPTIONAL: Code from your skin for a busy indicator e.g.
        <control type="group">
            <visible>Container(9999).IsUpdating</visible>
            <visible>!Window.IsVisible(DialogVideoInfo.xml)</visible>
            <include>Dialog_Busy</include>
        </control>
        -->

    </controls>
</window>
```


## Onclick Action to open info for TMDbHelper ListItems
```xml
<onclick>RunScript(plugin.video.themoviedb.helper,add_path=$INFO[ListItem.FolderPath],call_auto=1190)</onclick>
```
This action retrieves the tmdb_id and tmdb_type from the listitem path to call the lookup.


## Onclick Action to open info for a search query
```xml
<onclick>RunScript(plugin.video.themoviedb.helper,add_query=$INFO[ListItem.Label],tmdb_type=person,call_auto=1190)</onclick>
```
This action will look-up the tmdb_id based upon the query and tmdb_type. If multiple items are found, it will present the user with a dialog box to select the correct one. The path constructed with the tmdb_id is then passed to the add_path method.

When using add_query, you must specify `tmdb_type=movie|tv|person`


## Onclick Action to open info for a specific DBID  
```xml
<onclick>RunScript(plugin.video.themoviedb.helper,add_dbid=$INFO[ListItem.DBID],tmdb_type=movie,call_auto=1190)</onclick>
```

🔖 v6.8.18+ 

This action adds a skinvariables json rpc lookup for the DBID to allow for adding items based on local library information (rather than online lookups).

When using add_dbid, you must specify `tmdb_type=movie|tv|season|episode|collection`


## Onclick Action to open info for a specific TMDb ID
```xml
<onclick>RunScript(plugin.video.themoviedb.helper,add_tmdb=$INFO[ListItem.UniqueID(tmdb)],tmdb_type=movie,call_auto=1190)</onclick>
```

🔖 v6.8.18+ 

This action adds the tmdb_id directly to be constructed as a path. It can be useful to call the online lookup from the library or other plugins.

When using add_tmdb, you must specify `tmdb_type=movie|tv|person`



## Person Info

```
String.IsEqual(ListItem.Property(item.tmdb_type),person)
String.IsEqual(ListItem.Property(tmdb_type),person)
```

Since Kodi doesn't have a DialogPersonInfo, the DialogVideoInfo dialog will be used to display information about people. Your skin will need to modify the video info dialog to show relevant info for people. One of the above conditions can be used for this purpose.

Note that `type` params (and all variations such as `item.type`) are depreciated in v5+ to be replaced with the more specific `tmdb_type` naming. In v6+ the depreciated `type` param will be removed entirely. This change is to avoid namespace clashes with the python function name `type`

## Closing the window manager and info dialog

```
<onclick>RunScript(plugin.video.themoviedb.helper,close_dialog=1190)</onclick>
```

Use the above command to stop the window manager, close the info dialog, and close out the custom window.

While the window manager is active, any time the info dialog closes it will attempt to reopen the info dialog with the previous item in history. This behaviour will interfere with actions that require the info dialog to be closed (e.g. playing a movie or browsing a tvshow) and so the above command must be used to close out the window manager first.


## Direct Call Auto

```
Skin.SetBool(TMDbHelper.DirectCallAuto)
```

🔖 v5.1.13+ 


This setting improves speed by generating a ListItem internally and open the info dialog directly (rather than place it in the custom window list and wait for Kodi to update the list).

When using this method, you can remove the list ID "9999" from your custom window as it will not be used. 

Because the custom window 1190 will not have a Container with a ListItem, depending on how your skin functions, the background will also be blank. One possible workaround is to include you background directly in DialogVideoInfo.xml using a conditional check for the custom window, e.g.

```
<include condition="Window.IsVisible(1190)">Background_Include</include>
```