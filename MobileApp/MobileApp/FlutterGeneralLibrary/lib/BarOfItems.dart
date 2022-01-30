import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class BarOfProductCategories extends StatelessWidget {
  List<String> items;
  void Function(int) callback;

  static int selectedIndex = 0;
  BarOfProductCategories(this.items, this.callback);

  build(context) => Container(
        height: 50,
        child: ListView.builder(
            itemCount: items.length,
            scrollDirection: Axis.horizontal,
            itemBuilder: (context, index) {
              return Container(
                padding: EdgeInsets.all(10),
                child: RaisedButton(
                  color: index == selectedIndex ? Colors.grey : Colors.grey[300],
                  onPressed: () {
                    callback(index);
                  },
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(10)),
                  child: Text(items[index]),
                ),
              );
            }),
      );
}
