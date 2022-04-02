// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility that Flutter provides. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:mobile_app/main.dart';
import 'package:mobile_app/model/ServerGateway.dart';
import 'package:mobile_app/model/exception/UserWithIdDoesNotExist.dart';
import 'package:mobile_app/pages/LoginPage.dart';
import 'package:mobile_app/pages/SplashPage.dart';
import 'package:mobile_app/pages/StartWidget.dart';

void main() {

  ServerGateway.initializeWithRealImplementation = false;





  testWidgets('print test', (WidgetTester tester) async {
    print("hi ");
  });

  testWidgets('server gateway will return null as signed in user at the start!', (WidgetTester tester) async {
    print("hi 1");
    var gateway = await ServerGateway.instance();
    print("hi 2");
    expect(gateway.signedInUser,null);
  });


  testWidgets('sign in will throw no such user exception when the user is not registered', (WidgetTester tester) async {
    ServerGateway.initializeWithRealImplementation = false;
    await tester.pumpWidget(StartWidget());
    await tester.pump(Duration(seconds: 5));
    var gateway = ServerGateway.instance();

    print("hi 1");
    try{
      print("hi 2");
      await gateway.signIn("some user id", "some password");
      print("hi 3");
    }catch (e)
    {
      print("-----");
      if(!(e is UserWithIdDoesNotExist))
        throw Exception("we expected to throw UserWithIdDoesNotExist exception");
    }


  });


  testWidgets('user will be prompted with empty warning if userid left empty', (WidgetTester tester) async {

    const TEST_MOCK_STORAGE = './test/fixtures/core';
    const channel = MethodChannel('plugins.flutter.io/path_provider');


    tester.binding.defaultBinaryMessenger.setMockMethodCallHandler(channel,(MethodCall methodCall) async {
      return TEST_MOCK_STORAGE;
    });

    await tester.pumpWidget(StartWidget());
    await tester.pump(Duration(seconds: 15));
    await tester.tap(find.widgetWithText(Text,"Login"));
    expect(find.text('user id cannot be empty'), findsOneWidget);
  });
}
