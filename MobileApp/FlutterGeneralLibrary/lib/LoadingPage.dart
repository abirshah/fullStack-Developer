

import 'dart:async';

import 'package:flutter_general/LoadingWidget.dart';
import 'package:flutter_general/PercentageOfParent.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';


typedef FutureArrived = void Function (dynamic value);
typedef FutureFailed = void Function ();

class LoadingPage extends StatelessWidget
{
  final FutureArrived? futureArrived;
  final FutureFailed? futureFailed;
  final Future future;

  LoadingPage._(this.future , {this.futureArrived , this.futureFailed});


  build(context)
  {
    prepareFuture(context);

    return Center(child: LoadingWidget(),);
  }

  void prepareFuture(BuildContext context) {
    future.then((value){

      if(futureArrived!=null)
        futureArrived!(value);

      Navigator.pop(context);
    },onError: (value){

      if(futureFailed!=null)
        futureFailed!();

      Navigator.pop(context);
    });
  }
}

Future showLoadingPage(context,Future future,{FutureArrived? futureArrived ,FutureFailed? futureFailed })
{
  return Navigator.push(context, MaterialPageRoute(fullscreenDialog: true,
      builder:(c)=> LoadingPage._(future,futureArrived: futureArrived,futureFailed: futureFailed)
  ));
}
