"""Publish verified local ZIP filenames and a read-only disk cleanup guide."""
import hashlib
import json
from pathlib import Path
import shutil
from datetime import datetime,timezone
from audit_handoff_disk import size_tree

ROOT=Path(__file__).resolve().parents[1]


def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(8*1024*1024),b''):h.update(block)
    return h.hexdigest()


def main():
    previous=json.loads((ROOT/'provenance/qa/handoff_packages_preliminary_20261102.json').read_text())
    checks=json.loads((ROOT/'provenance/qa/handoff_packages_verification_20261102.json').read_text())
    if checks['status']!='PASS':raise ValueError('Finish verification first')
    finalized={}
    for kind in ['development','overleaf']:
        row=previous[kind];source=Path(row['partial_path']).resolve();target=Path(row['final_path']).resolve()
        if not source.is_relative_to((ROOT/'tmp').resolve()) or target.parent!=Path('D:/').resolve():raise ValueError('Unexpected export path')
        if target.exists():raise FileExistsError('Preserve existing final ZIP')
        if sha(source)!=row['sha256']:raise ValueError('Changed verified partial ZIP')
        source.rename(target)  # Only this task's new file, never a source directory.
        target.with_suffix('.zip.sha256').write_text(row['sha256']+'  '+target.name+'\n',encoding='ascii')
        finalized[kind]={**row,'path':str(target),'final_sha256':sha(target)}
        assert finalized[kind]['final_sha256']==row['sha256']
    initial=json.loads((ROOT/'provenance/qa/handoff_disk_inventory_20261102.json').read_text())
    rows={Path(r['path']).name:r for r in initial['directories']}
    temp=size_tree(ROOT/'tmp');project=size_tree(ROOT);paperbuild=size_tree(ROOT/'paper/build')
    usage=shutil.disk_usage('D:/')
    guide=Path('D:/ARC2-Global_Keep_Archive_Cleanup_20261102.md')
    gib=lambda n:f'{n/2**30:.2f}'
    text=[
        '# ARC2-Global — giữ, lưu Drive và dọn ổ D (2/11/2026)','',
        f"Ổ D: tổng **{gib(usage.total)} GiB**, còn trống **{gib(usage.free)} GiB** sau khi tạo ZIP. Không thư mục gốc nào đã bị xóa.",'',
        '## Hai gói mới','',
        '| File | Dung lượng | Dùng để |','|---|---:|---|',
        f"| {Path(finalized['development']['path']).name} | {gib(finalized['development']['bytes'])} GiB | Giao bạn tiếp tục paper/code; có START_HERE.md, lịch sử Git, bằng chứng R3 và TC1L, cache MiniLM |",
        f"| {Path(finalized['overleaf']['path']).name} | {finalized['overleaf']['bytes']/2**20:.2f} MiB | Upload Overleaf, chọn main.tex; có LaTeX/bibliography/vector figures và supplement TC1L |",'',
        'Đã kiểm tra hash7110file trong gói development, bảo toàn6258file được manifestR3 ghi nhận; compile Overleaf độc lập16trang, khớp nội dung/kích thước trang bản hiện tại. Table fragmentTC1L cũng compile và đã được xem trực quan.','',
        '**Bản thảo chính chưa chèn TC1L và chưa bổ sung GCPA.** Hai việc này nằm trong START_HERE.md để người nhận hoàn thiện. Gói development là bản giao nội bộ, không phải artifact công khai ẩn danh.','',
        '## Nên giữ và lưu lên Drive trước','',
        '| Thư mục/file | Dung lượng khảo sát | Khuyến nghị |','|---|---:|---|',
        f"| D:/ARC2-B1c-R3-backup-20261030 | {gib(rows['ARC2-B1c-R3-backup-20261030']['logical_bytes'])} GiB | Lưu Drive/archive riêng: checkpoints, vectors và lịch sử backup lớn không có đầy đủ trong ZIP development |",
        f"| D:/ARC2-B2-backup-20261031 | {gib(rows['ARC2-B2-backup-20261031']['logical_bytes'])} GiB | Lưu Drive/archive riêng: bằng chứng và dữ liệu server của B2 |",
        f"| D:/DASFAA-2027-paper | {gib(project['logical_bytes'])} GiB hiện tại, gồm tmp {gib(temp['logical_bytes'])} GiB | Giữ làm workspace gốc; khi lưu Drive có thể bỏ tmp/build. Một số raw G replay/container lớn chỉ còn ở workspace/backups, không nằm hết trong ZIP |",
        f"| D:/DASFAA-2027-MixIndex | {gib(rows['DASFAA-2027-MixIndex']['logical_bytes'])} GiB | Lưu Drive nếu giữ toàn bộ provenance/nghiên cứu cũ. Gói giao mới đã có query MiniLM và snapshot skill ARIS cần thiết |",
        '| Hai ZIP mới và file .sha256 đi kèm | Khoảng1.45GiB tổng cộng | Ưu tiên upload để giao bạn và phục hồi phần paper hiện tại |','',
        'Hai backup lớn cộng **181.18 GiB**. Chỉ dọn bản local sau khi xác nhận upload đủ, đối chiếu file/dung lượng và kiểm tra tải lại được. ZIP development không thay thế hai backup này cho mọi nhu cầu tái chạy H100.','',
        'Trong B1c backup: artifacts khoảng60.51GiB, snapshots khoảng65.26GiB. Chưa chứng minh từng snapshot trùng byte hoàn toàn; không coi toàn bộ snapshots là rác chỉ vì tên giống nhau.','',
        '## Không còn cần cho công việc paper hiện tại / có thể dọn local','',
        '| Đường dẫn | Khi nào có thể dọn |','|---|---|',
        f"| D:/DASFAA-2027-paper/tmp/ | {gib(temp['logical_bytes'])} GiB: gói thử, Git bundle staging, bản extract để QA. Sau khi hai ZIP mới được giữ an toàn, thư mục tạm này không cần cho source paper |",
        f"| D:/DASFAA-2027-paper/paper/build/ | {gib(paperbuild['logical_bytes'])} GiB: build/render có thể tạo lại. PDF chính và source nằm ngoài build |",
        '| D:/DASFAA-2027-paper-release/ | Bản export cũ; dữ liệu scientific được manifest ghi nhận đã có trong R3 và gói development mới |',
        '| D:/DASFAA-2027-paper-release-20261101-r3-paper-story/ | Bản giải nén của release cũ. Toàn bộ6258file manifest đã được giữ qua mapping trong gói development mới |',
        '| D:/DASFAA-2027-paper-release-20261101.zip | ExportR1 đã được thay thế; không cần để tiếp tục bài hiện tại |',
        '| D:/DASFAA-2027-paper-release-20261101-r2-complete.zip | ExportR2 đã được thay thế; không cần để tiếp tục bài hiện tại |',
        '| D:/DASFAA-2027-paper-release-20261101-r3-paper-story.zip | Gói mới đã chứa toàn bộ manifestR3. Có thể giữ một bản trên Drive cho lịch sử, rồi dọn local |',
        '| D:/DASFAA-2027-paper-before-arc2-global-20261025/ | Snapshot draft cũ khoảng2MiB; tùy nhu cầu lưu lịch sử, không phải bản đang viết |',
        '| D:/mixindex-cargo/ và D:/mixindex-diskann3-source/ | Không cần cho mapper paper/exact retrieval hiện tại; archive trước nếu còn giữ hướng ANN/systems cũ |','',
        'Các file .receipt.json/.sha256 của release cũ là sidecar; giữ chung nếu lưu ZIP cũ, hoặc dọn chung khi đã quyết định bỏ bản export đó.','',
        'Đối chiếu manifest của các ZIPR1/R2/R3 và release folder: không có file scientific được manifest ghi nhận ở các bản trước bị thiếu hoặc đổi hash so với R3. Điều này không phải tuyên bố mọi file tạm/check ngoài manifest đều giống nhau.','',
        '## Nên giữ nếu còn dùng','',
        f"D:/graph4paper khoảng{gib(rows['graph4paper']['logical_bytes'])}GiB: thư viện/skill thiết kế hình dùng chung. Không cần để compile Overleaf vì figurePDF/TikZ đã nằm trong gói; nên giữ nếu tiếp tục thiết kế figure.",'',
        'Các dự án, tài liệu cá nhân và game khác trên D không được xếp vào danh sách xóa của cuộc rà soát này.','',
        '## Kiểm tra ZIP sau khi tải từ Drive','',
        'Đối chiếu SHA256 với file .zip.sha256 đi kèm. Gói development còn có handoff/verify_package.py để kiểm tra toàn bộ member của ZIP hoặc folder đã giải nén. Không cần H100 để kiểm tra gói.','',
        'Báo cáo máy: provenance/qa/handoff_packages_verification_20261102.json và handoff_old_export_comparison_20261102.json trong workspace gốc.','']
    guide.write_text('\n'.join(text),encoding='utf-8')
    receipt={'status':'COMPLETE','client_date':'2026-11-02','utc':datetime.now(timezone.utc).isoformat(),
             'source_snapshot_commit':previous['source_commit'],'packages':finalized,'verification':checks,
             'disk_after':{'free_bytes':usage.free,'used_bytes':usage.used,'total_bytes':usage.total},
             'guide':str(guide),'original_folders_deleted':0,'source_paper_unchanged':True,
             'supplement_visual_check':'Parent inspected compiled table PNG; no overflow/clipping observed'}
    (ROOT/'provenance/qa/handoff_delivery_20261102.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':receipt['status'],'files':{k:v['path'] for k,v in finalized.items()},'free_GiB':usage.free/2**30,'guide':str(guide)},indent=2))


if __name__=='__main__':main()
