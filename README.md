<!-- badges: start -->
![](https://img.shields.io/github/created-at/cielivb/ImageViewer?color=yellow)
![](https://img.shields.io/github/last-commit/cielivb/ImageViewer?color=yellow)
![](https://img.shields.io/github/commit-activity/t/cielivb/ImageViewer?color=yellow)
![](https://img.shields.io/github/contributors/cielivb/ImageViewer?color=yellow)
![](https://img.shields.io/github/languages/top/cielivb/ImageViewer?color=yellow)
<!--![Github License](https://img.shields.io/github/license/cielivb/ImageViewer?color=yellow)--> <!--Shows unspecified?-->
<!-- badges: end -->

# ImageViewer
ImageViewer is a widget module developed using WxPython which lets the user zoom and pan across a single image in a similar manner to using Google Maps. 

ImageViewer was developed with the intention of implementing it as part of a larger personal WxPython GUI application project. In the larger application, one or more ImageViewers can be opened in response to one or more events, for example, a button press as demonstrated in the example videos below. ImageViewer is not intended to be a 'gallery explorer' which traverses across image files in a given directory. It is intended as a tool to aid in the visual inspection of a single image file. I will likely rename ImageViewer to something like ImageInspector in the future.

Future enhancements could include restricting users from panning infinitely far away from the image, the option to apply contrast enhancement masks, and the ability to save a local copy of images. 

<details>
  <summary>Test App Example Video 1</summary>
  
  Demonstrating pan and zoom ability on multiple ImageViewer instances.

  
  https://github.com/user-attachments/assets/43e27f91-a555-49a6-add6-c06e6aa7dbd1
  
</details>

<details>
  <summary>Test App Example Video 2</summary>
  
  Demonstrating pan and zoom ability as well as resize behaviour on a single ImageViewer instance.

  
  https://github.com/user-attachments/assets/5f5f83a6-4f26-4976-9f94-ce98c05a0ebd
  
</details>



## How to Use ImageViewer
tests.py contains the code for a tiny WxPython app that implements the core functionality of ImageViewer. Use this as your key reference point. Key points to note:
- Put ImageViewer.py in the same directory as your WxPython script
- Import ImageViewer.py into your WxPython script, e.g., <code>import ImageViewer as iv</code>
- Set your binding/s
- In your event handler, call <code>iv.view(parent=self, image_file='imagepath')</code>, and an ImageViewer displaying the image located at your imagepath should appear.

You will need to install the following packages if you don't already have them: wx, numpy, pillow.


## Credits
This logic behind this project took much inspiration from [this C++ demo example](https://forums.wxwidgets.org/viewtopic.php?p=196414#p196414). Credits also to the [WxPython docs](https://docs.wxpython.org/index.html), the [WxWidgets docs](https://docs.wxwidgets.org/stable/), and the mountains of discussion forums on these sites!

## License
This project is under the [MIT License](LICENSE). 
