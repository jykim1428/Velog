import feedparser
import git
import os

# 벨로그 RSS 피드 URL
# example : rss_url = 'https://api.velog.io/rss/@rimgosu'
rss_url = 'https://api.velog.io/rss/@jykim1428'

# 깃허브 레포지토리 경로
repo_path = '.'

# 'velog-posts' 폴더 경로
posts_dir = os.path.join(repo_path, 'velog-posts')

# 'velog-posts' 폴더가 없다면 생성
if not os.path.exists(posts_dir):
    os.makedirs(posts_dir)

# 레포지토리 로드
repo = git.Repo(repo_path)

# RSS 피드 파싱
feed = feedparser.parse(rss_url)

# 각 글을 파일로 저장하고 커밋
for entry in feed.entries:
    try:
        # 파일 이름에서 유효하지 않은 문자 제거 또는 대체
        file_name = entry.title if entry.title else "untitled"  # 제목이 없으면 "untitled"
        file_name = file_name.replace('/', '-')  # 슬래시를 대시로 대체
        file_name = file_name.replace('\\', '-')  # 백슬래시를 대시로 대체
        # 필요에 따라 추가 문자 대체
        file_name += '.md'
        file_path = os.path.join(posts_dir, file_name)

        # 글 내용 가져오기 (description이 없으면 summary 사용)
        content = getattr(entry, 'description', None) or getattr(entry, 'summary', None)

        # 내용이 있는 경우에만 파일 작성
        if content and not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)  # 글 내용을 파일에 작성

            # 깃허브 커밋
            repo.git.add(file_path)
            repo.git.commit('-m', f'Add post: {entry.title if entry.title else "untitled"}')

    except Exception as e:
        print(f"Error processing entry: {e}")
