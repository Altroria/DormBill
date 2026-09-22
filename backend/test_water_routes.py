"""Test water_expenses router import and registration"""
try:
    from app.routers import water_expenses
    print('✓ water_expenses imported')
    print(f'Router type: {type(water_expenses.router)}')
    print(f'Routes count: {len(water_expenses.router.routes)}')
    for route in water_expenses.router.routes:
        print(f'  - {route.path} {route.methods}')
except Exception as e:
    print(f'✗ Error: {e}')
    import traceback
    traceback.print_exc()

print("\n--- Testing main app ---")
try:
    from app.main import app
    water_routes = [r for r in app.routes if 'water-expenses' in r.path]
    print(f'Water-expenses routes in app: {len(water_routes)}')
    for route in water_routes:
        print(f'  - {route.path}')
except Exception as e:
    print(f'✗ Error: {e}')
    import traceback
    traceback.print_exc()
