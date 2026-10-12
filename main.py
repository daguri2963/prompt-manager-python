"""터미널에서 실행하는 간단한 프롬프트 관리 프로그램."""

CATEGORIES = ["텍스트 생성", "이미지 생성", "영상 생성", "페르소나", "자동화", "기타"]


def initial_prompts():
    """프로그램 실행마다 같은 예시 데이터로 시작한다."""
    return [
        {
            "title": "블로그 글 초안 작성",
            "content": (
                "당신은 친절한 블로그 편집자입니다. 주제를 받으면 초보자도 이해할 수 있는 "
                "제목 3개와 서론, 본론, 결론으로 된 글 초안을 작성해주세요. "
                "확인되지 않은 사실은 단정하지 마세요."
            ),
            "category": "텍스트 생성",
            "favorite": False,
        },
        {
            "title": "제품 이미지 아이디어",
            "content": (
                "제품명과 특징을 받으면 제품의 장점을 보여주는 이미지 구도 3개를 제안해주세요. "
                "각 구도에 배경, 조명, 카메라 각도, 색감을 포함해주세요."
            ),
            "category": "이미지 생성",
            "favorite": False,
        },
        {
            "title": "학습 도우미 페르소나",
            "content": (
                "당신은 처음 배우는 사람을 돕는 튜터입니다. 어려운 용어를 먼저 쉬운 말로 설명하고, "
                "한 번에 한 단계씩 안내해주세요. 각 단계 끝에는 이해 여부를 확인해주세요."
            ),
            "category": "페르소나",
            "favorite": False,
        },
    ]


def show_menu():
    print("\n=== 나만의 프롬프트 관리 ===")
    print("1. 프롬프트 추가")
    print("2. 프롬프트 목록")
    print("3. 카테고리별 조회")
    print("4. 프롬프트 검색")
    print("5. 프롬프트 상세 보기")
    print("6. 즐겨찾기 설정/해제")
    print("7. 즐겨찾기 목록")
    print("0. 종료")


def nonempty_input(message):
    while True:
        value = input(message).strip()
        if value:
            return value
        print("빈 값은 입력할 수 없습니다. 다시 입력해주세요.")


def available_categories(prompts):
    """기본 카테고리 뒤에 사용자가 추가한 카테고리를 붙인다."""
    categories = CATEGORIES.copy()
    for prompt in prompts:
        if prompt["category"] not in categories:
            categories.append(prompt["category"])
    return categories


def choose_category(prompts, allow_custom=False):
    categories = available_categories(prompts)
    print("\n카테고리 선택:")
    for number, category in enumerate(categories, start=1):
        print(f"{number}. {category}")
    if allow_custom:
        print(f"{len(categories) + 1}. 직접 입력")

    while True:
        choice = input("번호 선택: ").strip()
        if choice.isdecimal():
            number = int(choice)
            if 1 <= number <= len(categories):
                return categories[number - 1]
            if allow_custom and number == len(categories) + 1:
                name = nonempty_input("새 카테고리 이름: ")
                for category in categories:
                    if category.casefold() == name.casefold():
                        return category
                return name
        print("목록에 있는 번호를 입력해주세요.")


def add_prompt(prompts):
    print("\n=== 프롬프트 추가 ===")
    title = nonempty_input("제목: ")
    content = nonempty_input("내용: ")
    category = choose_category(prompts, allow_custom=True)
    prompts.append(
        {"title": title, "content": content, "category": category, "favorite": False}
    )
    print("프롬프트가 추가되었습니다.")


def format_prompt_row(index, prompt):
    """목록, 검색, 즐겨찾기에서 같은 번호와 표시 형식을 사용한다."""
    star = " ⭐" if prompt["favorite"] else ""
    return f"{index + 1}. [{prompt['category']}] {prompt['title']}{star}"


def print_prompt_rows(prompts, selected=None):
    """번호는 언제나 전체 목록의 번호를 사용한다."""
    if selected is None:
        selected = range(len(prompts))
    selected = list(selected)
    if not selected:
        print("표시할 프롬프트가 없습니다.")
        return
    for index in selected:
        print(format_prompt_row(index, prompts[index]))
    print(f"총 {len(selected)}개")


def show_list(prompts):
    print("\n=== 프롬프트 목록 ===")
    print_prompt_rows(prompts)


def show_category(prompts):
    print("\n=== 카테고리별 조회 ===")
    category = choose_category(prompts)
    print(f"\n[{category}] 프롬프트:")
    selected = [i for i, prompt in enumerate(prompts) if prompt["category"] == category]
    print_prompt_rows(prompts, selected)


def search_prompt(prompts):
    print("\n=== 프롬프트 검색 ===")
    keyword = nonempty_input("검색어: ").casefold()
    selected = [
        i
        for i, prompt in enumerate(prompts)
        if keyword in prompt["title"].casefold()
        or keyword in prompt["content"].casefold()
    ]
    print("\n검색 결과:")
    print_prompt_rows(prompts, selected)


def select_prompt_index(prompts):
    if not prompts:
        print("저장된 프롬프트가 없습니다.")
        return None
    print_prompt_rows(prompts)
    value = input("프롬프트 번호: ").strip()
    if not value.isdecimal() or not 1 <= int(value) <= len(prompts):
        print("올바른 프롬프트 번호를 입력해주세요.")
        return None
    return int(value) - 1


def show_detail(prompts):
    print("\n=== 프롬프트 상세 보기 ===")
    index = select_prompt_index(prompts)
    if index is None:
        return
    prompt = prompts[index]
    print(f"제목: {prompt['title']}")
    print(f"카테고리: {prompt['category']}")
    print(f"즐겨찾기: {'⭐' if prompt['favorite'] else '아니요'}")
    print("내용:")
    print(prompt["content"])


def toggle_favorite(prompts):
    print("\n=== 즐겨찾기 설정/해제 ===")
    index = select_prompt_index(prompts)
    if index is None:
        return
    prompt = prompts[index]
    prompt["favorite"] = not prompt["favorite"]
    action = "추가" if prompt["favorite"] else "해제"
    print(f"'{prompt['title']}'의 즐겨찾기를 {action}했습니다.")


def show_favorites(prompts):
    print("\n=== 즐겨찾기 목록 ===")
    selected = [i for i, prompt in enumerate(prompts) if prompt["favorite"]]
    print_prompt_rows(prompts, selected)


def main():
    prompts = initial_prompts()
    actions = {
        "1": add_prompt,
        "2": show_list,
        "3": show_category,
        "4": search_prompt,
        "5": show_detail,
        "6": toggle_favorite,
        "7": show_favorites,
    }
    while True:
        show_menu()
        choice = input("선택: ").strip()
        if choice == "0":
            print("프로그램을 종료합니다.")
            break
        action = actions.get(choice)
        if action is None:
            print("메뉴에 있는 번호를 입력해주세요.")
        else:
            action(prompts)


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\n프로그램을 종료합니다.")
