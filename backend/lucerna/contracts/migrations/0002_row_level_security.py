from django.db import migrations

# GUC set per request in PostgresRlsMiddleware. If unset, COALESCE yields -1 (no rows visible).
_CMP = (
    "clearance_required <= "
    "COALESCE(NULLIF(current_setting('lucerna.clearance_level', true), ''), '-1')::int"
)

_APPLY_SQL = [
    "ALTER TABLE contracts_contract ENABLE ROW LEVEL SECURITY",
    "ALTER TABLE contracts_contract FORCE ROW LEVEL SECURITY",
    "DROP POLICY IF EXISTS lucerna_contract_select ON contracts_contract",
    f"CREATE POLICY lucerna_contract_select ON contracts_contract FOR SELECT USING ({_CMP})",
    "DROP POLICY IF EXISTS lucerna_contract_insert ON contracts_contract",
    f"CREATE POLICY lucerna_contract_insert ON contracts_contract FOR INSERT WITH CHECK ({_CMP})",
    "DROP POLICY IF EXISTS lucerna_contract_update ON contracts_contract",
    f"CREATE POLICY lucerna_contract_update ON contracts_contract FOR UPDATE USING ({_CMP}) WITH CHECK ({_CMP})",
    "DROP POLICY IF EXISTS lucerna_contract_delete ON contracts_contract",
    f"CREATE POLICY lucerna_contract_delete ON contracts_contract FOR DELETE USING ({_CMP})",
    "ALTER TABLE contracts_deadline ENABLE ROW LEVEL SECURITY",
    "ALTER TABLE contracts_deadline FORCE ROW LEVEL SECURITY",
    "DROP POLICY IF EXISTS lucerna_deadline_select ON contracts_deadline",
    f"CREATE POLICY lucerna_deadline_select ON contracts_deadline FOR SELECT USING ({_CMP})",
    "DROP POLICY IF EXISTS lucerna_deadline_insert ON contracts_deadline",
    f"CREATE POLICY lucerna_deadline_insert ON contracts_deadline FOR INSERT WITH CHECK ({_CMP})",
    "DROP POLICY IF EXISTS lucerna_deadline_update ON contracts_deadline",
    f"CREATE POLICY lucerna_deadline_update ON contracts_deadline FOR UPDATE USING ({_CMP}) WITH CHECK ({_CMP})",
    "DROP POLICY IF EXISTS lucerna_deadline_delete ON contracts_deadline",
    f"CREATE POLICY lucerna_deadline_delete ON contracts_deadline FOR DELETE USING ({_CMP})",
]

_REVERT_SQL = [
    "DROP POLICY IF EXISTS lucerna_deadline_delete ON contracts_deadline",
    "DROP POLICY IF EXISTS lucerna_deadline_update ON contracts_deadline",
    "DROP POLICY IF EXISTS lucerna_deadline_insert ON contracts_deadline",
    "DROP POLICY IF EXISTS lucerna_deadline_select ON contracts_deadline",
    "ALTER TABLE contracts_deadline NO FORCE ROW LEVEL SECURITY",
    "ALTER TABLE contracts_deadline DISABLE ROW LEVEL SECURITY",
    "DROP POLICY IF EXISTS lucerna_contract_delete ON contracts_contract",
    "DROP POLICY IF EXISTS lucerna_contract_update ON contracts_contract",
    "DROP POLICY IF EXISTS lucerna_contract_insert ON contracts_contract",
    "DROP POLICY IF EXISTS lucerna_contract_select ON contracts_contract",
    "ALTER TABLE contracts_contract NO FORCE ROW LEVEL SECURITY",
    "ALTER TABLE contracts_contract DISABLE ROW LEVEL SECURITY",
]


def apply_rls(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        return
    for sql in _APPLY_SQL:
        schema_editor.execute(sql)


def revert_rls(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        return
    for sql in _REVERT_SQL:
        schema_editor.execute(sql)


class Migration(migrations.Migration):
    dependencies = [
        ("contracts", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(apply_rls, revert_rls),
    ]
