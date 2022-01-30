import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'dart:math';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';
import 'package:path_provider/path_provider.dart';
import 'package:shimmer/shimmer.dart';



Future<File> saveAssetToLocalFile(String assetFileAbsPath,String generatedFileName,{bool returnFileIfAlreadyExists = true}) async{
  final data = await rootBundle.load(assetFileAbsPath);
  final buffer = data.buffer;
  Directory tempDir = await getTemporaryDirectory();
  String tempPath = tempDir.path;
  var filePath = tempPath + generatedFileName;
  var file = new File(filePath);

  if(await file.exists() && returnFileIfAlreadyExists)
    return file;

  return file.writeAsBytes(buffer.asUint8List(data.offsetInBytes, data.lengthInBytes));
}


void printTimeSince(int sinceTimeMillis,{String message = ""})
{
  print("$message time=${currentTimeMillis-sinceTimeMillis}Ms");
}

Decoration roundRectangleDecoration(double radius, Color strokeColor,
        {Color backgroundColor = Colors.transparent, double borderWidth = 1}) =>
    ShapeDecoration(
        color: backgroundColor,
        shape: RoundedRectangleBorder(
            side: BorderSide(color: strokeColor, width: borderWidth),
            borderRadius: BorderRadius.circular(radius)));

navigateUnNamed(Widget widget, BuildContext context) {
  Navigator.push(context, MaterialPageRoute(builder: (context) => widget));
}

int get currentTimeMillis => DateTime.now().millisecondsSinceEpoch;

String randomString(int length) {
  var result = "";
  var random = Random(currentTimeMillis);

  for (int i = 1; i <= length; i++)
    result += String.fromCharCode((random.nextInt(30) + 65));

  return result;
}

double percentageOfDeviceHeight(context, double percent) =>
    MediaQuery.of(context).size.height * percent;

double percentageOfDeviceWidth(context, double percent) =>
    MediaQuery.of(context).size.width * percent;

String toBase64(String str) {
  var bytes = utf8.encode(str);
  var base64Str = base64.encode(bytes);
  return base64Str;
}

Future<T> showLoadingPageWhileCompleting<T>(context, Future<T> future) {
  var completed = false;

  future.then((v) {
    completed = true;
    Navigator.pop(context);
  }, onError: (e) {
    completed = true;
    Navigator.pop(context);
  });

  showDialog(
      context: context,
      barrierDismissible: false,
      builder: (c) => WillPopScope(
            onWillPop: () async {
              return completed;
            },
            child: Align(
              alignment: Alignment.center,
              child: SizedBox(
                height: percentageOfDeviceWidth(context, 0.2),
                width: percentageOfDeviceWidth(context, 0.2),
                child: CircularProgressIndicator(
                  valueColor: AlwaysStoppedAnimation<Color>(Color(0xfff06627)),
                ),
              ),
            ),
          ));

  return future;
}

StreamSubscription<bool> showLoadingPageBaseOnStreamStatus(
    context, Stream<bool> showLoadingStatusStream) {
  Completer<bool>? completer;

  var subscription = showLoadingStatusStream.listen((event) {
    if (event) {
      if (completer == null) {
        completer = new Completer<bool>();
        showLoadingPageWhileCompleting(context, completer!.future);
      }
    } else if (completer != null) {
      completer!.complete();
      completer = null;
    }
  });

  subscription.onDone(() {
    if (completer != null) completer!.complete(null);
  });

  return subscription;
}

String decorateWithThousandSeparator(String number) {
  String output = "";
  int count = 0;
  for (int i = number.length - 1; i >= 0; i--) {
    count++;
    output = number[i] + output;
    if (count == 3) {
      count = 0;
      if (i != 0) output = "," + output;
    }
  }

  return output;
}

Widget wrapItInALoadingPageOnTopWhichInterceptsTouch(Widget widget, context,
    {bool isLoadingNow = true,
    Color colorOverlay = const Color(0x3f000000),
    Color loadingColor = const Color(0xfff06627),
    double clipRadius = 3.0}) {
  return Stack(
    children: [
      IgnorePointer(
        child: widget,
        ignoring: isLoadingNow,
      ),
      if (isLoadingNow)
        Positioned.fill(
          child: ClipRRect(
            borderRadius: BorderRadius.circular(clipRadius),
            child: Container(
              color: colorOverlay,
              child: Align(
                alignment: Alignment.center,
                child: SizedBox(
                  height: percentageOfDeviceWidth(context, 0.1),
                  width: percentageOfDeviceWidth(context, 0.1),
                  child: CircularProgressIndicator(
                    valueColor: AlwaysStoppedAnimation<Color>(loadingColor),
                  ),
                ),
              ),
            ),
          ),
        ),
    ],
  );
}

Widget wrapItInAShimmerPageOnTopWhichInterceptsTouch(Widget widget, context,
    {bool isLoadingNow = true,
    Color shimmerBaseColor = Colors.white,
     Color? shimmerHighlightColor,
    double clipRadius = 3.0,
    double shimmerOpacity = 0.35}) {
  return Stack(
    children: [
      IgnorePointer(
        child: widget,
        ignoring: isLoadingNow,
      ),
      if (isLoadingNow)
        Positioned.fill(
          child: Opacity(
            opacity: shimmerOpacity,
            child: ClipRRect(
              borderRadius: BorderRadius.circular(clipRadius),
              child: Shimmer.fromColors(
                  child: Container(
                    color: Colors.white,
                  ),
                  baseColor: shimmerBaseColor,
                  highlightColor: shimmerHighlightColor==null?Theme.of(context).accentColor:shimmerHighlightColor),
            ),
          ),
        ),
    ],
  );
}




extension IterableExtension<K,V> on Iterable<MapEntry<K,V>>
{
  Map<K,V> toMap()
  {
    Map<K,V> map = {};

    this.forEach((element) {
      map[element.key] = element.value;
    });

    return map;
  }
}


extension ListOfListsExtension<K> on List<List<K>>
{
  List<K> flatList()
  {
    List<K> list = <K>[];

    this.forEach((element) {
      list.addAll(element);
    });

    return list;
  }
}



extension ListExtension<K> on List<K>
{
  List<K> concat(List<K> anotherList)
  {
    this.addAll(anotherList);
    return this;
  }

  List<K> concatElement(K anotherValue)
  {
    this.add(anotherValue);
    return this;
  }

  int count(bool Function(K) predicate)
  {
    var count = 0;
    forEach((element) {
      if(predicate(element))
        count++;
    });
    return count;
  }

  K? min(num Function(K) evaluator)
  {
    if(isEmpty)
      return null;

    var min = evaluator(first);
    var result = first;

    forEach((element) {
      var number = evaluator(element);
      if(number < min)
      {
        min = number;
        result = element;
      }
    });

    return result;
  }

  K? max(num Function(K) evaluator)
  {
    if(isEmpty)
      return null;

    var max = evaluator(first);
    var result = first;

    forEach((element) {
      var number = evaluator(element);
      if(number > max)
      {
        max = number;
        result = element;
      }
    });

    return result;
  }
}
