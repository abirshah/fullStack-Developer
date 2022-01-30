import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';

import 'Utils.dart';


class FutureValue<T>
{
  final FutureOr<T> Function() computation;
  final String key ;
  final int timeoutMillis;


  FutureValue({required this.computation , this.timeoutMillis = 99999999999999,required this.key  });

  toString() => "FutureValue(key=$key)";
}

typedef TouchInterceptorLoadingWrapperOnTopOfWidget = Widget Function(BuildContext context,Widget contentWidget,bool isLoadingNow);


class FutureWidget<T> extends StatefulWidget {

  ///you should pass one of Future , FutureOr , FutureValue values
  ///null is not accepted
  ///
  /// you can pass FutureValue and specify key to prevent repeatedly evaluations
  /// and also you can pass timeout for last evaluated value causing reevaluation!
  final dynamic future;
  final Widget Function(BuildContext, dynamic) builder;
  final Widget Function(BuildContext ,Exception error)? errorBuilder;

  final double initialLoadingBoxHeight;
  final double initialLoadingBoxWidth;
  final TouchInterceptorLoadingWrapperOnTopOfWidget? touchInterceptorLoadingWrapperOnTopOfWidget;

  FutureWidget({
    this.future,
    required this.builder,
    this.errorBuilder ,
    this.touchInterceptorLoadingWrapperOnTopOfWidget ,
    this.initialLoadingBoxWidth = double.infinity,
    this.initialLoadingBoxHeight = 100
  })
      :super(key:(future is FutureValue && future.key!=null ? ValueKey(future.key) : null))
  {

    if(!(future !=null
        || future is Future
        || future is FutureOr
        || future is FutureValue))
      throw Exception("future should be one of : Future , FutureOr , FutureValue !");

  }

  createState() => FutureWidgetState<T>();
}

class FutureWidgetState<T> extends State<FutureWidget> {
  static const String  _NotEvaluatedSign ="value is not evaluated yet!";
  dynamic value = _NotEvaluatedSign;
  dynamic lastEvaluatedValue;
  Widget? lastEvaluatedWidget;
  dynamic lastError;
  int _lastEvaluatedValueTimeMillis = 0;

  void initState() {
    super.initState();
    _evaluateFuture();
  }

  void didUpdateWidget(FutureWidget oldWidget) {
    super.didUpdateWidget(oldWidget);

    if ((_isValueNotEvaluated() && !_futureFailed()) || widget.future is! FutureValue)
       _evaluateFuture();
  }

  _evaluateFuture() {
    value = _NotEvaluatedSign;
    lastError = null;

    final future = (widget.future is FutureValue) ? widget.future.computation() : widget.future;

    future.then((v) {
      value = v;
      lastEvaluatedValue = v;
      _lastEvaluatedValueTimeMillis = currentTimeMillis;
      _setStateIfMounted();
    }).catchError((error) {
      lastError = error;
      _setStateIfMounted();
      throw error;
    });
  }

  _setStateIfMounted(){
    if(mounted)
      setState(() {});
  }

  _isValueNotEvaluated() =>  value == _NotEvaluatedSign || isExpired();

  bool isExpired() =>
      (widget.future is FutureValue)  &&
      currentTimeMillis - _lastEvaluatedValueTimeMillis > widget.future.timeoutMillis ;

  _isValueEvaluated() => !_isValueNotEvaluated();

  _futureFailed() => lastError != null;

  _reEvaluateFuture()
  {
    value = _NotEvaluatedSign;
    lastError = null;

    _setStateIfMounted();

    _evaluateFuture();
  }

  build(context)
  {
    if (_isValueEvaluated())
    {
      //wrapping in shimmer widget no matter what.preventing element tree change and widget disposal
      lastEvaluatedWidget = widget.builder(context,  value as T);
      return _wrapInLoadingWidget(context,lastEvaluatedWidget!,false);
    }
    else if(_futureFailed())
    {
      if(widget.errorBuilder != null)
        return widget.errorBuilder!(context,  lastError);
      else
        return createDefaultErrorWidget();
    }
    else
      return
         lastEvaluatedWidget != null ? _wrapInLoadingWidget( context,lastEvaluatedWidget!,true):createLoadingWidget(context);
  }

  Widget _wrapInLoadingWidget(BuildContext context,Widget currentWidget,bool isLoadingNow)
  {
    if(widget.touchInterceptorLoadingWrapperOnTopOfWidget!=null)
      return widget.touchInterceptorLoadingWrapperOnTopOfWidget!(context,currentWidget,isLoadingNow);

    return wrapItInAShimmerPageOnTopWhichInterceptsTouch(currentWidget,context,isLoadingNow: isLoadingNow);
  }

  createDefaultErrorWidget() => widget.future is! FutureValue ?  Center(
    child: Column(
      mainAxisSize: MainAxisSize.min,
      children: <Widget>[
        Icon(Icons.error_outline,color: Colors.red,),
      ],),
  ): Center(
    child: RaisedButton(
      onPressed: (){_reEvaluateFuture();},
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: <Widget>[
          Icon(Icons.sync,color: Colors.deepOrange,),
          Text("Retry",)
        ],),
    ),
  );

  createLoadingWidget(context) => _wrapInLoadingWidget(context,
    Container(width: widget.initialLoadingBoxWidth,height: widget.initialLoadingBoxHeight,),true
  );


}
