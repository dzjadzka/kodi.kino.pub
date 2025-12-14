## Scripted Recommendations

TMDbHelper v5+ provides a scripted recommendations window as an alternative to the [call_auto/add_path method](https://github.com/jurialmunkey/plugin.video.themoviedb.helper/wiki/Replacing-Extended-Info) of replacing extended info. 

The advantage of the recommendation dialog is faster widget loading and simplified window management. However, due to the scripted nature of the dialog, it comes with several disadvantages in terms of limited usage flexibility.

**NOTE**  
The recommendation dialog cannot be mixed with the call_auto method as the window management routines will conflict.


**DISCLAIMER**

I have not touched the code for the recommendations dialog in several years and do not intended to further develop this code. The recommendations dialog was always intended as an experimental feature and requires skins to follow a very specific and limiting pattern of using the info dialog.

When using the recommendations script, there is an expectation that users alternate between "info dialog > recommendations dialog > info dialog > recommendations dialog". If this alternating usage pattern suits your skin and your skin will always follow this pathway, then great! 

However, if you want greater flexibility in the pathways taken between info dialogs, using the recommendations dialog is, ironically, not recommended. Use the [call_auto/add_path method](https://github.com/jurialmunkey/plugin.video.themoviedb.helper/wiki/Replacing-Extended-Info) if you prefer to keep a more flexible skinning approach which allows for better interaction with native non-scripted functionality in Kodi.


## Setup

### Background window

The recommendations window requires a custom window to act as the background layer behind the info dialog. This window should contain whatever you would normally include for the background of your media windows. There are no required controls or restrictions on what you place in this window.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<window type="window" id="1191">
    <controls>
        <include>Background_Main</include>
    </controls>
</window>
```

Any window ID can be used for this window (I'm using 1191 here). This window will be active as the background window layer behind the info dialog whilst the recommendations script is actively managing the info dialog windows.


### Recommendations dialog

The recommendations dialog is a separate window which will contain all the related widget lists for your info dialog. It is activated via a runscript command. Create a dialog in your skin called script-tmdbhelper-recommendations.xml and add some empty lists with unique IDs to it. These lists will be filled by the script when we call it. The lists should not have any onclick actions or similar as these will be managed by the script.


```
script-tmdbhelper-recommendations.xml
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<window type="dialog">
    <defaultcontrol always="true">6000</defaultcontrol>
    <controls>
        <control type="grouplist" id="6000">
            <control type="list" id="5000">
                <include>MyPosterListDefinition</include>
            </control>
            <control type="list" id="5001">
                <include>MyPosterListDefinition</include>
            </control>
        </control>
    </controls>
</window>
```

There are no restrictions or required controls in this window. You can add as many or few lists as you require, and in whatever configuration that you like. In the above I have created two lists inside a grouplist but this is merely an example.


## Running the script

The recommendations dialog is called from the info dialog via a RunScript command.

```
Runscript(plugin.video.themoviedb.helper,recommendations=5000|info=cast|true|info,window_id=1191,tmdb_type=movie,tmdb_id=348)
```

| Param | Required | Description |
| :--- | :--- | :--- |
| window_id={id} | Required | The id of the base window to be used as the background |
| tmdb_type={type}<br>tmdb_id={id} | Required | Details of the item the recommendations window will be based upon.<br>Standard [lookup query params](https://github.com/jurialmunkey/plugin.video.themoviedb.helper/wiki/Lists-Additional-Params#lookup-parameters) can be used here if the tmdb_id is not known. |
| recommendations={id\|endpoint\|related\|action} | Required | The definition of the lists to load. Separate multiple list definitions by using a double pipe `\|\|` [See below for further details](https://github.com/jurialmunkey/plugin.video.themoviedb.helper/wiki/Recommendations-Dialog#recommendations-params). |
| context={builtin} | Optional | The Kodi builtin to call when contextmenu button is pressed e.g. `context=SetFocus(9000)` will set focus to control 9000 when the contextmenu button is pressed. If omitted the contextmenu button will perform same action as select |
| setproperty={name} | Optional | Sets `Window(Home).Property(TMDbHelper.{name})` to True when the user clicks an item to open a new info dialog. Can be useful if you need to set a property to trigger a specific type of animation |
| winprop_{name}={value} | Optional | Sets the local `Window.Property({name})` for the recommendations dialog. Can add as many as you like e.g. `winprop_genre=$INFO[ListItem.Genre],winprop_studio=$INFO[ListItem.Studio]` will set the genre and studio from the info dialog to the recommendations dialog `Window.Property(genre)` and `Window.Property(studio)` |


### Recommendations Params

```
recommendations=id|endpoint|related|action
```

| Param | Description |
| :--- | :--- |
| id | Content will be added to this list ID in `script-tmdbhelper-recommendations.xml` |
| endpoint | Content will be retrieved from this info= endpoint. Any TMDbHelper info= path can be used. |
| related | Set to true when using a [related list endpoint](https://github.com/jurialmunkey/plugin.video.themoviedb.helper/wiki/Lists-Related) to automatically add the item lookup params to the path |
| action | The action to perform when the user clicks an item in the list. Can be `info` `play` `browse` `text` or a Kodi builtin command. |


**Example**  
```
recommendations=5000|info=cast|true|info||5001|info=similar|true|play
```

* Adds info=cast to list id="5000" and info=similar to list id="5001".
* Cast action when clicking will open info dialog. Similar movies action will play
* Both lists have related as true because the related lookup params should be added.

info=cast will become  
```
plugin://plugin.video.themoviedb.helper/?info=cast&tmdb_type=movie&tmdb_id=348&nextpage=false&fanarttv=false&cacheonly=true
```


More complex paths can also be used, for instance discover paths:

**Example**  
```
recommendations=5000|info=discover&tmdb_type=movie&with_genres=$INFO[ListItem.Genre]|false|info
```

The lookup params will not be added to this list since related is set to false. In this case the list becomes:  
```
plugin://plugin.video.themoviedb.helper/?info=discover&tmdb_type=movie&with_genres=$INFO[ListItem.Genre]&nextpage=false&fanarttv=false&cacheonly=true
```

### Window Properties

As the window is scripted the standard Container.IsUpdating status will not work. Instead, the script will set window properties so that you can determine the status of each list. In addition, there are two home properties which are set to assist with window transition animations.

| Property | Description |
| :--- | :--- |
| `String.IsEqual(Window.Property(List_5000_IsUpdating),True)` | Will be True while list id="5000" IsUpdating (replace 5000 for each ID) |
| `String.IsEqual(Window.Property(List_5000_Visible),True)` | Will be True once items have been added to list id="5000" (replace 5000 for each ID) |
| `String.IsEqual(Window.Property(List_Main_Visible),True)` | Will be True once all lists have started updating |
| `String.IsEqual(Window(Home).Property(TMDbHelper.Recommendations.HideInfo),True)` | Will be True when transitioning from Info to Recommendations |
| `String.IsEqual(Window(Home).Property(TMDbHelper.Recommendations.HideRecs),True)` | Will be True when transitioning from Recommendations to Info |


### Additional Commands

The skin can use the `onaction` endpoint to close the recommendations window manager to perform a builtin which requires the info dialog to be closed.

```
RunScript(plugin.video.themoviedb.helper,recommendations=onaction,builtin={builtin},window_id={window_id})
```

By default the builtin will be executed first and then the info dialog closed. Specifying the optional `after` param will reverse the order and wait until the info dialog is closed before performing the builtin.

**Example**  
```
RunScript(plugin.video.themoviedb.helper,recommendations=onaction,builtin=SendClick(8),window_id=1191)
```

This command will click the play button (id=8) and then close any active recommendations/info dialogs. 

**Example**  
```
RunScript(plugin.video.themoviedb.helper,recommendations=onaction,builtin=PlayMedia($INFO[ListItem.FolderPath]),window_id=1191,after)
```

This command will first close any recommendations/info dialogs and *then* do the PlayMedia() command.


### Opening Info Outside of Recommendations

Occasionally it might be desirable to open the info dialog and window management outside of the recommendations window. For instance from a widget inside a custom window or via an info button on the videoosd. This can be acheived via the `oninfo` endpoint. Standard query lookup params can be used if the tmdb_id is unknown.

```
RunScript(plugin.video.themoviedb.helper,recommendations=oninfo,window_id=1191,tmdb_type={type},tmdb_id={id})
```

**Example**  
```
RunScript(plugin.video.themoviedb.helper,recommendations=oninfo,window_id=1191,tmdb_type=movie,tmdb_id=348)
```

**Example**  
```
RunScript(plugin.video.themoviedb.helper,recommendations=oninfo,window_id=1191,tmdb_type=movie,query=Alien,year=1979)
```


### UnManaged TMDbHelper Lists

On occasion it might be desirable to set a list container using a TMDbHelper path but that is not managed by the main script. For instance, you might like to display a sublist based upon the currently focused item in another list.

TMDbHelper does not place any restrictions on additional lists in the scripted window so you can achieve this using a normal `<content>$INFO[Container(ID).ListItem.FolderPath]</content>` widget. 

However, you might also wish to have any clicks on this list managed by TMDbHelper via one of the standard info|play|browse|text actions. To define the action for an unmanaged list you can set a Action_{id} window property onload of the recommendations window

**Example**  
```
<onload>SetProperty(Action_5095,info)</onload>
```

Sets the list with id="5095" to use the standard `info` action


### UnManaged Non-TMDbHelper Lists

Additionally, there are also no restriction on adding lists from plugins other than TMDbHelper via the normal `<content>` tags.

Note that unlike standard media windows, Container.IsUpdating for these lists will initially be false rather than true. The container will only begin updating after the main dialog has initialized. 

As a result `<visible>Container(ID).IsUpdating | !Integer.IsEqual(Container(ID).NumItems,0)</visible>` will be false onload and the container will never update. To get around this issue, you should keep the container visible until the List_Main_Visible property is set.

```
<visible>String.IsEmpty(Window.Property(List_Main_Visible)) | Container(ID).IsUpdating | !Integer.IsEqual(Container(ID).NumItems,0)</visible>
```

If you need to close the window manager to perform an action, remember to run the `recommendations=onaction` command.

```xml
<onclick>RunScript(plugin.video.themoviedb.helper,recommendations=onaction,window_id={window_id})</onclick>
<onclick>YOUR ONCLICK COMMAND GOES HERE</onclick>
```
