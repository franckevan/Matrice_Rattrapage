import json
import unittest

from i2.dashboard import render_dashboard
from i2.generate_dataset import MALFORMED, build_lines
from i2.metrics import compute_metrics
from i2.normalize import normalize_date, normalize_record, process


def run(lines):
    res = process(lines)
    return res, compute_metrics(res)


def sess(**kw):
    base = {"id": "x", "date": "2026-10-19", "period": "am", "group": "A", "mode": "DG",
            "title": "T", "domain": "web", "teacherId": "t1", "status": "confirmed"}
    base.update(kw)
    return json.dumps(base)


class JeuFourni(unittest.TestCase):
    def setUp(self):
        self.res, self.m = run(build_lines())

    def test_dataset_a_12_lignes_dont_la_derniere_malformee(self):
        lines = build_lines()
        self.assertEqual(len(lines), 12)
        self.assertEqual(lines[-1], MALFORMED)

    def test_compteurs(self):  # assertion 1
        self.assertEqual((self.m["accepted"], self.m["rejected"], self.m["duplicates"]), (6, 4, 2))
        self.assertEqual({r["line"] for r in self.res.rejected}, {7, 8, 9, 12})
        self.assertEqual([d["id"] for d in self.res.duplicates], ["s01", "s02"])

    def test_seances_par_domaine(self):
        self.assertEqual(self.m["sessions_by_domain"], {"cyber": 1, "data": 1, "projet": 2, "web": 2})

    def test_heures_formateur_sans_auto(self):  # assertion 2
        self.assertEqual(self.m["teacher_hours"], {"t1": 7.0, "t2": 7.0, "t3": 3.5})

    def test_heures_apprenant(self):  # assertion 3
        self.assertEqual(self.m["learner_hours"], {"A": 14.0, "B": 14.0})

    def test_taux_confirmation(self):  # assertion 4
        self.assertEqual(self.m["confirmation"], {"confirmed": 3, "assigned": 5, "rate": 0.6})


class Normalisation(unittest.TestCase):
    def test_dates(self):
        self.assertEqual(normalize_date("19/10/2026"), "2026-10-19")
        self.assertEqual(normalize_date("2026-10-19"), "2026-10-19")
        for bad in ("2026-02-30", "31/04/2026", "2026-1-5", "", None):
            with self.assertRaises(ValueError):
                normalize_date(bad)

    def test_periodes_et_statuts(self):
        rec, err = normalize_record(json.loads(sess(period="après-midi", status="confirme")))
        self.assertEqual((err, rec["period"], rec["status"]), ([], "pm", "confirmed"))

    def test_regles_auto_et_confirmed(self):
        _, e1 = normalize_record(json.loads(sess(mode="AUTO", status="proposed")))  # AUTO + formateur
        _, e2 = normalize_record(json.loads(sess(teacherId=None, status="confirmed")))
        self.assertTrue(e1 and e2)

    def test_valider_avant_dedupliquer(self):
        res, _ = run([sess(id="a", period="soir"), sess(id="a")])  # 1re occurrence invalide
        self.assertEqual((len(res.accepted), len(res.rejected), len(res.duplicates)), (1, 1, 0))

    def test_creneaux_distincts(self):  # groupe A + Promotion sur le même créneau = 1 seul créneau
        _, m = run([sess(id="a", group="A"), sess(id="b", group="Promotion", teacherId="t2")])
        self.assertEqual(m["learner_hours"], {"A": 3.5, "B": 3.5})


class CasVide(unittest.TestCase):
    def test_cas_vide(self):
        res, m = run([])
        self.assertEqual((m["accepted"], m["rejected"], m["duplicates"]), (0, 0, 0))
        self.assertIsNone(m["confirmation"]["rate"])
        self.assertEqual(m["teacher_hours"], {})
        self.assertIn("non applicable", render_dashboard(m, res.rejected, res.duplicates))

    def test_que_des_auto_denominateur_nul(self):
        _, m = run([sess(mode="AUTO", teacherId=None, status="proposed")])
        self.assertIsNone(m["confirmation"]["rate"])


if __name__ == "__main__":
    unittest.main()
