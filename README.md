<!-- badges: start -->
![](https://img.shields.io/github/created-at/cielivb/ImageInspector?color=yellow)
![](https://img.shields.io/github/last-commit/cielivb/ImageInspector?color=yellow)
![](https://img.shields.io/github/commit-activity/t/cielivb/ImageInspector?color=yellow)
![](https://img.shields.io/github/contributors/cielivb/ImageInspector?color=yellow)
![](https://img.shields.io/github/languages/top/cielivb/ImageInspector?color=magenta)
![Github License](https://img.shields.io/github/license/cielivb/ImageInspector?color=yellow)
<!-- badges: end -->

# ImageInspector

## About ImageInspector
ImageInspector is a widget module developed using WxPython that lets the user zoom and pan across a single image in a similar manner to using Google Maps. 

ImageInspector enables the user to: 
- View a single .png, .jpg, or .webp image
- Use click and release (including via touchscreen) to pan across an image
- Double click to zoom in
- Click on +/- buttons to zoom in and out
- Use touchscreen pinch gesture to zoom in and out
- Reset image state using the reset button


### Example Videos using included Test App
<details>
  <summary>Test App Example Video 1</summary>
  
  Demonstrating pan and zoom ability on multiple ImageInspector instances.

  
  https://github.com/user-attachments/assets/43e27f91-a555-49a6-add6-c06e6aa7dbd1
  
</details>

<details>
  <summary>Test App Example Video 2</summary>
  
  Demonstrating pan and zoom ability as well as resize behaviour on a single ImageInspector instance.

  
  https://github.com/user-attachments/assets/5f5f83a6-4f26-4976-9f94-ce98c05a0ebd
  
</details>

### ImageInspector Motivation
ImageInspector was developed with the intention of implementing it as part of a larger personal WxPython GUI application project. In the larger application, one or more ImageInspectors can be opened in response to one or more events, for example, a button press as demonstrated in the example videos below. ImageInspector is not intended to be a 'gallery explorer' which traverses across image files in a given directory. It is intended as a tool to aid in the visual inspection of a single image file. 

### Future enhancements
Future enhancements could include expanding the range of viewable image file types, restricting users from panning infinitely, adding an option to apply contrast enhancement masks, and adding a save image feature.



## How to Use ImageInspector
You will need to install the following packages if you don't already have them: wx, numpy, pillow. ImageInspector has been specifically tested on Python 3.13.5, wxPython 4.2.4, numpy 2.2.6, pillow 12.0.0.

tests.py contains the code for a tiny WxPython app that implements ImageInspector. Use this as your reference. You will first need to import ImageInspector into your wxPython script. In your event handler, call <code>image_inspector.view(parent=self, image_file='imagepath')</code>. An ImageInspector displaying the image at your imagepath should appear.



## Credits
This logic behind this project took much inspiration from [this C++ demo example](https://forums.wxwidgets.org/viewtopic.php?p=196414#p196414). Credits also to the [WxPython docs](https://docs.wxpython.org/index.html), the [WxWidgets docs](https://docs.wxwidgets.org/stable/), and the mountains of discussion forums on these sites!

## License
This project is under the [MIT License](LICENSE). 
