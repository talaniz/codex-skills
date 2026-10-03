import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('workflow', Path(__file__).resolve().parents[1] / 'scripts/workflow.py')
w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)

def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], text=True, stderr=subprocess.PIPE).strip()

class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        git(self.repo, 'init', '-b', 'main')
        git(self.repo, 'config', 'user.name', 'Fixture')
        git(self.repo, 'config', 'user.email', 'fixture@example.invalid')
        self.write('app.py', 'print("hello")\n')
        self.write('harness/active/demo/phase.md', '[App](../../../app.py)\n[Sibling](review.md#result)\n')
        self.write('harness/active/demo/review.md', '# Result\nSynthetic independent evidence\n')
        self.write('README.md', '[Phase](harness/active/demo/phase.md#done)\n')
        self.commit()
        self.head = git(self.repo, 'rev-parse', 'HEAD')
        self.record = {'id':'demo','status':'completed','recorded_by':'main-agent','reviewed_head':self.head,
            'required_checks':['fixture'], 'checks':[{'name':'fixture','status':'passed','head':self.head}],
            'reviews':[{'role':'code','reviewer':'reviewer-a','verdict':'sign-off','head':self.head,'evidence':'https://example.invalid/code'},
                       {'role':'e2e','reviewer':'reviewer-b','verdict':'sign-off','head':self.head,'evidence':'https://example.invalid/e2e'}],
            'files':['harness/active/demo/phase.md','harness/active/demo/review.md']}
        self.save_record()

    def write(self, path, text):
        p = self.repo / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)

    def commit(self):
        git(self.repo, 'add', '.')
        git(self.repo, 'commit', '-m', 'fixture')

    def save_record(self):
        self.write('harness/milestone.json', json.dumps(self.record))
        self.commit()

    def test_preview_and_apply_preserve_links_and_evidence(self):
        before = git(self.repo, 'status', '--porcelain')
        plan = w.preview(self.repo)
        self.assertEqual(len(plan['moves']), 2)
        self.assertEqual(git(self.repo, 'status', '--porcelain'), before)
        w.apply(self.repo, plan['digest'], 'Owner authorized archive')
        self.assertFalse((self.repo/'harness/active/demo/phase.md').exists())
        self.assertTrue((self.repo/'harness/active/demo').is_dir())
        self.assertEqual((self.repo/'harness/archive/demo/phase.md').read_text(), '[App](../../../app.py)\n[Sibling](review.md#result)\n')
        self.assertIn('harness/archive/demo/phase.md#done', (self.repo/'README.md').read_text())
        self.assertEqual(json.loads((self.repo/'harness/milestone.json').read_text())['status'], 'archived')

    def test_rejects_incomplete_milestone(self):
        self.record['status']='active'; self.save_record()
        with self.assertRaises(ValueError): w.preview(self.repo)

    def test_rejects_missing_or_same_reviewer(self):
        self.record['reviews'][1]['reviewer']='reviewer-a'; self.save_record()
        with self.assertRaises(ValueError): w.preview(self.repo)

    def test_rejects_failed_check(self):
        self.record['checks'][0]['status']='failed'; self.save_record()
        with self.assertRaises(ValueError): w.preview(self.repo)

    def test_rejects_product_changes_after_review(self):
        self.write('app.py','print("changed")\n'); self.commit()
        with self.assertRaises(ValueError): w.preview(self.repo)

    def test_rejects_dirty_and_stale_digest(self):
        plan=w.preview(self.repo)
        self.write('new.txt','unrelated')
        with self.assertRaises(ValueError): w.apply(self.repo,plan['digest'],'Authorized')
        (self.repo/'new.txt').unlink()
        self.record['recorded_by']='different-main'; self.save_record()
        with self.assertRaises(ValueError): w.apply(self.repo,plan['digest'],'Authorized')

    def test_rejects_traversal_and_symlinks(self):
        self.record['files']=['../outside']; self.save_record()
        with self.assertRaises(ValueError): w.preview(self.repo)

    def test_rejects_symlink_source(self):
        p=self.repo/'harness/active/demo/phase.md';p.unlink();p.symlink_to(self.repo/'app.py');self.commit()
        with self.assertRaises(ValueError): w.preview(self.repo)

    def test_rejects_unsupported_reference_links(self):
        self.write('README.md','[Phase][p]\n\n[p]: harness/active/demo/phase.md\n');self.commit()
        self.record['reviewed_head']=git(self.repo,'rev-parse','HEAD')
        for r in self.record['reviews']+self.record['checks']: r['head']=self.record['reviewed_head']
        self.save_record()
        with self.assertRaises(ValueError): w.preview(self.repo)

    def test_rejects_archive_collision(self):
        self.write('harness/archive/demo/phase.md','existing')
        with self.assertRaises(ValueError): w.preview(self.repo)

    def test_apply_requires_reason(self):
        plan=w.preview(self.repo)
        with self.assertRaises(ValueError):w.apply(self.repo,plan['digest'],' ')

    def test_rolls_back_caught_write_failure(self):
        plan=w.preview(self.repo)
        original=w.write_bytes
        calls=[]
        def fail_once(path,data):
            calls.append(path)
            if len(calls)==2:raise OSError('injected failure')
            return original(path,data)
        w.write_bytes=fail_once
        try:
            with self.assertRaises(OSError):w.apply(self.repo,plan['digest'],'Authorized')
        finally:w.write_bytes=original
        self.assertEqual(git(self.repo,'status','--porcelain'),'')
        self.assertTrue((self.repo/'harness/active/demo/phase.md').is_file())

    def test_inventory_is_read_only(self):
        old=git(self.repo,'status','--porcelain')
        result=w.inspect(self.repo)
        self.assertEqual(result['branch'],'main')
        self.assertFalse(result['dirty'])
        self.assertEqual(git(self.repo,'status','--porcelain'),old)
        self.write('app.py','dirty')
        self.assertTrue(w.inspect(self.repo)['dirty'])

    def test_rejects_stale_review(self):
        self.record['reviews'][0]['head']='a'*40;self.save_record()
        with self.assertRaises(ValueError):w.preview(self.repo)

    def test_rejects_missing_review(self):
        self.record['reviews'].pop();self.save_record()
        with self.assertRaises(ValueError):w.preview(self.repo)

    def test_rejects_detached_head(self):
        git(self.repo,'checkout','--detach')
        with self.assertRaises(ValueError):w.preview(self.repo)

    def reviewed_fixture_change(self, text):
        self.write('README.md',text);self.commit()
        self.record['reviewed_head']=git(self.repo,'rev-parse','HEAD')
        for r in self.record['reviews']+self.record['checks']:r['head']=self.record['reviewed_head']
        self.save_record()

    def test_rejects_ambiguous_autolink(self):
        self.reviewed_fixture_change('<harness/active/demo/phase.md>\n')
        with self.assertRaises(ValueError):w.preview(self.repo)

    def test_rejects_nested_link_syntax(self):
        self.reviewed_fixture_change('[Phase](harness/active/demo/phase.md "title (nested)")\n')
        with self.assertRaises(ValueError):w.preview(self.repo)

    def test_rejects_link_inside_code_example(self):
        self.reviewed_fixture_change('```md\n[Phase](harness/active/demo/phase.md)\n```\n')
        with self.assertRaises(ValueError):w.preview(self.repo)
