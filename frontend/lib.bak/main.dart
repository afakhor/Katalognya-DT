import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

// Ganti dengan IP laptop/server kamu pas testing
// Contoh termux: http://localhost:8000
const String BASE_URL = 'http://localhost:8000';

void main() => runApp(const KatalogApp());

class KatalogApp extends StatelessWidget {
  const KatalogApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Katalog DT',
      theme: ThemeData(useMaterial3: true, colorSchemeSeed: Colors.blue),
      home: const ProductPage(),
    );
  }
}

class ProductPage extends StatefulWidget {
  const ProductPage({super.key});
  @override
  State<ProductPage> createState() => _ProductPageState();
}

class _ProductPageState extends State<ProductPage> {
  List products = [];
  Map<int, int> cart = {};
  bool loading = true;

  @override
  void initState() {
    super.initState();
    loadProducts();
  }

  Future<void> loadProducts() async {
    setState(() => loading = true);
    try {
      final res = await http.get(Uri.parse('$BASE_URL/products'));
      if (res.statusCode == 200) {
        setState(() => products = jsonDecode(res.body));
      }
    } catch (_) {}
    setState(() => loading = false);
  }

  Future<void> submitPO() async {
    if (cart.isEmpty) return;
    final items = cart.entries.map((e) => {'product_id': e.key, 'qty': e.value}).toList();
    final res = await http.post(
      Uri.parse('$BASE_URL/po'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'items': items}),
    );
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(res.statusCode == 200? 'PO terkirim' : 'Gagal: ${res.statusCode}')),
    );
    if (res.statusCode == 200) setState(() => cart.clear());
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Katalog DT')),
      body: loading
         ? const Center(child: CircularProgressIndicator())
          : ListView.builder(
              itemCount: products.length,
              itemBuilder: (c, i) {
                final p = products[i];
                final id = p['id'] as int;
                final qty = cart[id]?? 0;
                return ListTile(
                  title: Text(p['name']?? 'Produk $id'),
                  subtitle: Text('Rp ${p['price']?? 0}'),
                  trailing: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      IconButton(
                        icon: const Icon(Icons.remove),
                        onPressed: qty > 0? () => setState(() => cart[id] = qty - 1) : null,
                      ),
                      Text('$qty'),
                      IconButton(
                        icon: const Icon(Icons.add),
                        onPressed: () => setState(() => cart[id] = qty + 1),
                      ),
                    ],
                  ),
                );
              },
            ),
      bottomNavigationBar: Padding(
        padding: const EdgeInsets.all(12),
        child: FilledButton(
          onPressed: cart.isEmpty? null : submitPO,
          child: Text('Kirim PO (${cart.values.fold(0, (a, b) => a + b)} item)'),
        ),
      ),
    );
  }
}
