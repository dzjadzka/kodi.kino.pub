## Service Monitor

TMDbHelper provides a ListItem service monitor that provides details about the current item from online APIs. By default, the service monitor will be in an idle state. To use the service monitor, enable the skin setting `TMDbHelper.Service` in your skin. You can also disable some parts of the service monitor such as additional artwork lookups if not needed.

| Command | Description |
| :--- | :--- |
| Skin.SetBool(TMDbHelper.Service) | Set service monitor to ACTIVE state |
| Skin.Reset(TMDbHelper.Service) | Set service monitor to IDLE state |
| Skin.ToggleSetting(TMDbHelper.Service) | Toggle state |
| Skin.ToggleSetting(TMDbHelper.EnableBlur) | [Enable blur image](https://github.com/jurialmunkey/plugin.video.themoviedb.helper/wiki/Service-Monitor#blur-monitor) |
| Skin.ToggleSetting(TMDbHelper.EnableDesaturate) | [Enable desaturated image](https://github.com/jurialmunkey/plugin.video.themoviedb.helper/wiki/Service-Monitor#desaturate-monitor) |
| Skin.ToggleSetting(TMDbHelper.EnableColors) | [Enable color monitor](https://github.com/jurialmunkey/plugin.video.themoviedb.helper/wiki/Service-Monitor#color-monitor) |
| Skin.ToggleSetting(TMDbHelper.DisableArtwork) | Disable additional artwork lookups |
| Skin.ToggleSetting(TMDbHelper.DisablePersonStats) | Disable kodi db person statistics |
| Skin.ToggleSetting(TMDbHelper.DisableExtendedProperties) | Disable additional properties such as Director.X.Name |
| !String.IsEmpty(Window(Home).Property(TMDbHelper.IsUpdating)) | Service Monitor is updating |
| String.IsEmpty(Window(Home).Property(TMDbHelper.IsUpdating)) | Service Monitor finished updating |
| SetProperty(TMDbHelper.WidgetContainer,WIDGET_ID,Home) | Specify a widget container ID to load info for. Note that the service monitor works automatically for dialogvideoinfo without a container ID specified. |
| Skin.ToggleSetting(TMDbHelper.ForceWidgetContainer) | Forces widget container ID lookup to be used in info dialog |
| SetProperty(TMDbHelper.ServicePause,1) | Pause the service monitor while the current window is active and has focus. Use with `<onload>` to stop a custom dialog from updating the service monitor. v4.4.34+ |
| Skin.SetBool(TMDbHelper.UseLocalWidgetContainer) | Enabling this setting will tell TMDbHelper to get the WidgetContainer property from the currently active window `Window.Property()` instead of from the home window `Window(Home).Property()` so that different widgetcontainer properties can be set for different windows. v5+ |
| Skin.SetString(TMDbHelper.MonitorContainer,99950) | Enables the alternate method where TMDbHelper will add the detailed item to a hidden container with the ID specified instead of using window properties. Any unqiue ID can be used, 99950 is an example. v5+ |


## Properties returned

As of v5, TMDbHelper has two methods for using the service monitor:
* The default "classic" method where info is set as a home window property
  * Window(Home).Property() is global and so can be accessed in any window.
* The experimental "container" method where a listitem is added to a hidden container.
  * Access details using standard listitem infolabel within local scope of current window.

NOTE: The container method is an experimental feature which is not recommended for stable use due to underlying bugs in exception handling for the Kodi xbmcgui module. As of of 6.8.0+ it also no longer has performance benefits and is potentially *slower* than the window property method.


### Classic method
TMDbHelper will output details to window properties on the home screen **$INFO[Window(Home).Property(TMDbHelper.ListItem.PROPERTY)]**

Replace "PROPERTY" with the property name from [Detailed Item Wiki Page](https://github.com/jurialmunkey/plugin.video.themoviedb.helper/wiki/Detailed-Item#general). Note that infolabels and infoproperties need to be converted as in the following examples:

| `$INFO[ListItem.Property(PROPERTY)]` | `$INFO[Window(Home).Property(TMDbHelper.ListItem.PROPERTY)]` |
| :--- | :--- |
| `$INFO[ListItem.Property(Cast.1.Name)]` | `$INFO[Window(Home).Property(TMDbHelper.ListItem.Cast.1.Name)]` |
| `$INFO[ListItem.Art(tvshow.clearart)]` | `$INFO[Window(Home).Property(TMDbHelper.ListItem.tvshow.clearart)]` |
| `$INFO[ListItem.Art(clearlogo)]` | `$INFO[Window(Home).Property(TMDbHelper.ListItem.clearlogo)]` |
| `$INFO[ListItem.Studio]` | `$INFO[Window(Home).Property(TMDbHelper.ListItem.Studio)]` |


### Container method
TMDbHelper adds the details to a hidden container as specified by `Skin.SetString(TMDbHelper.MonitorContainer,99950)`. Using this option allows access to the details via infolabels as a standard listitem.
**$INFO[Container(99950).ListItem.INFOLABEL]**

To use this method you must add a hidden list container with the specified ID on *every* window and dialog where you want to use the service monitor. If the active window does not have this container then TMDbHelper will idle until a window with the container becomes active.

```
<control type="list" id="99950">
   <itemlayout />
   <focusedlayout />
   <width>1</width>
   <height>1</height>
   <left>-1920</left>
</control>
```

See the [Detailed Item Wiki Page](https://github.com/jurialmunkey/plugin.video.themoviedb.helper/wiki/Detailed-Item#general) for a list of available properties.

### Player monitor

As of v4.6.44 it is also possible to get details of the now playing item by switching "ListItem" with "Player" in the window property **$INFO[Window(Home).Property(TMDbHelper.Player.PROPERTY)]**


### Special Additional Properties

Note: Syntax has changed as of v6.9+ 
For earlier versions replace dotted notation with underscores e.g. Premiered_Long vs. Premiered.Long

| Property | Description |
| :--- | :--- |
| Premiered.Long | Formatted with Kodi longdate settings |
| Premiered.Short | Formatted with "%d %b" |
| Premiered.Day | The full name of the day of the week (e.g. Monday) |
| Premiered.Day_Short | The short name for the day of the week (e.g. Mon) |
| Premiered.Year | Year only |
| Premiered.Custom | Premiered formatted using custom strftime `Skin.SetString(TMDbHelper.Date.Format,%d %b %Y)` see https://strftime.org/ for formatting string options. Will also apply custom formatting to `Next_Aired.Custom` and `Last_Aired.Custom` if airing data is available. |
| Premiered.Original | Lists date in original YYYY-MM-DD format |
| Duration.mins | Total Minutes e.g. 3hr12m will return 192 |
| Duration.H | Hours Portion e.g. 3hr12m will return 3 |
| Duration.M | Minutes Portion e.g. 3hr12m will return 12 |
| Duration.HHMM | Formatted HH:MM e.g. 3hr12m will return 03:12 |

### Watched Providers
Information is provided by JustWatch via the TMDb API for services on which the item is available for streaming, download, rent or buy. You *MUST* display the JustWatch logo and attribute this data as being from JustWatch whenever you use it.  


![](https://i.imgur.com/ORdr24P.png)

| Property | Description |
| :--- | :--- |
| Provider.X.Name | Name of the provider |
| Provider.X.Icon | Icon of the provider |
| Provider.X.Type | The format the provider has the item e.g. Rent, Buy, Flatrate |
| Provider.X.ID | The ID of the provider on JustWatch |

## Blur Monitor
TMDbHelper also provides a simple blur monitor.
```
Skin.ToggleSetting(TMDbHelper.EnableBlur)
```

### Source image
```
SetProperty(TMDbHelper.Blur.SourceImage,poster,Home)
```

| Key | Order of artwork used |
| :--- | :--- |
| thumb | Art(thumb) |
| poster | Art(tvshow.poster), Art(poster), Art(thumb) |
| fanart | Art(fanart), Art(thumb) |
| landscape | Art(landscape), Art(fanart), Art(thumb) |

The blurred artwork is taken from the active item in the service monitor. If you set a widget container ID property, it will take the source image for that item.

As of v2.4.37 it is possible to set a pipe `|` separated custom order of source artwork properties
```
SetProperty(TMDbHelper.Blur.SourceImage,Art(tvshow.fanart)|Art(fanart)|Art(tvshow.poster),Home)
```

### Fallback Source Image
```
SetProperty(TMDbHelper.Blur.Fallback,special://skin/extras/backgrounds/background.jpg,Home)
```
This image will be used for the blur if the specified source images are not available.

### Manual RunScript
```
RunScript(plugin.video.themoviedb.helper,blur_image=special://skin/extras/backgrounds/background.jpg)
```

### Output Blur Image
```
$INFO[Window(Home).Property(TMDbHelper.ListItem.BlurImage)]
$INFO[Window(Home).Property(TMDbHelper.ListItem.BlurImage.Original)]
$INFO[Container(99950).ListItem.Art(blurimage)
$INFO[Container(99950).ListItem.Art(blurimage.original)
```
Original contains the unblurred image to allow syncing of image change with blur

## Desaturate Monitor
Desaturate image. Usage is same as blur monitor. When using container method the output is added to ListItem.Art() instead.

| Desaturate Monitor | |
| :--- | :--- |
| Enable | `Skin.ToggleSetting(TMDbHelper.EnableDesaturate)` |
| Source | `SetProperty(TMDbHelper.Desaturate.SourceImage,poster,Home)` |
| Fallback | `SetProperty(TMDbHelper.Desaturate.Fallback,path/image.jpg,Home)` |
| Output Image | `$INFO[Window(Home).Property(TMDbHelper.ListItem.DesaturateImage)]` |
| Original Image | `$INFO[Window(Home).Property(TMDbHelper.ListItem.DesaturateImage.Original)]` |

## Color Monitor
Match colors of image. Usage is same as blur monitor.
Outputs main colour of image and a complimentary triadic colour using a 120 degree hue shift.
Luminance and Saturation values can be fixed to a floating point value between 0.0 and 1.0

| Color Monitor | |
| :--- | :--- |
| Enable | `Skin.ToggleSetting(TMDbHelper.EnableColors)` |
| Source | `SetProperty(TMDbHelper.Colors.SourceImage,poster,Home)` |
| Fallback | `SetProperty(TMDbHelper.Colors.Fallback,path/image.jpg,Home)` |
| Fixed Luminance (0.0 - 1.0) | `Skin.SetString(TMDbHelper.Colors.Luminance,0.75)` |
| Fixed Saturation (0.0 - 1.0) | `Skin.SetString(TMDbHelper.Colors.Saturation,0.75)` |
| Output Main | `$INFO[Window(Home).Property(TMDbHelper.ListItem.Colors.Main)]` |
| Output Complimentary | `$INFO[Window(Home).Property(TMDbHelper.ListItem.Colors.Comp)]` |