import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import os
import random
import schedule
import time
import threading
from datetime import datetime, timedelta, timezone

# 환경 변수 로드
load_dotenv()
TOKEN = os.environ.get('TOKEN_KEY')
USER_LIST = os.environ.get('USER_LIST')

CATEGORY_IDS = [
    1286215200214749205, 1289503899920891914, 1286202045904453723, 1178016892158492782, 
    1176211427820838970, 1204087799205339167, 1178017124304834732, 1184564611555524608,
    1223994343795327196, 1177986829639757874, 1259754856613281873, 1177987040529350817,
    1177987415953129562, 1177987089074245672, 1177987462455361537, 1227585629391556628,
    1178014263223271494, 1179109957711429632, 1177987530004639755, 1178011325973155961,
    1178783011358113803, 1176446283888738314, 1288522237095313459, 1291032817102356501, 
    1177987829381484704, 1184557520606474400, 1177987894519013376, 1177988015541469305,
    1177988053395050566, 1279460074611282095, 1279047238584107069, 1289871051949473834
]  # 삭제를 감지할 카테고리 ID
ROLE_IDS = [ 
    1294731852594024529, 1176439144130547793, 1176211427330109475, 1176211427330109473, 
    1211675617393774644, 1256781569738145964, 1265616454615830599, 1178743330461454426, 
    1200387953390800956, 1248281171842830448, 1261637387725832346, 1271369444635054090, 
    1293848612643803199, 1265616432688009247, 1176211427330109471, 1176211427300745224, 
    1176211427300745225, 1214890557759819806, 1285992466620612618, 1257050660969648198, 
    1256618551792369735, 1191294087412858880, 1176211427330109472, 1176448706078314527,
    1247503681708888146, 1288488740099981354, 1286979556754067486, 1286220050969399347,
    1286174278227722240, 1292044619839836281, 1286207854935670857, 1286208031335645194,
    1286208555187441727, 1286208490049900615, 1286184087425388626, 1176211427275575315,
    1240304978594103472, 1286211969946226770, 1286665271947563078, 1291314515035689032,
    1176211427275575311, 1176211427275575310, 1176211427275575309, 1176211427275575308,
    1176211427275575307, 1212784188181446747, 1258020230370820157, 1291774216726905008,
    1291774283030200340, 1291621072327802932, 1176211427246211100, 1176211427246211099,
    1286231598005489738, 1178771226664116264, 1176211427246211097, 1176211427246211096,
    1176211427246211095, 1176211427246211094, 1257238600266027098, 1279268223614849144,
    1179798687862497410, 1191083316779163648, 1201558913166868657, 1212400234718822441,
    1224008556047761529, 1234861618546872472, 1245708745900560384, 1256618323286949931,
    1286593432713691147, 1279405276717518948, 1288785880739352637, 1181252784083963994,
    1189929117613817987, 1268225917743005696, 1293258586901708820, 1284430473812246612,
    1181249948075970703, 1200814747398979695, 1213078664124698635, 1225464185832345680,
    1240136605822619688, 1216069161537765436, 1220350358640136305, 1286203751245418520,
    1189109949834473532, 1178762995095060490, 1178759222645751838, 1178776363973488670,
    1178776606437806120, 1183830343804014734, 1183822851954978916, 1183823073238065154,
    1183823250845872198, 1183825381929783325, 1183825458568102018, 1183825523693060157,
    1183827701379907646, 1183827860947992697, 1183828962607120484, 1183833649930580118,
    1183833289287544832, 1183833474239578243, 1183833528388034672, 1183833589952032878,
    1202286018959507507, 1202291626224132137, 1202282181246845018, 1217141291243143168,
    1217142069978730588, 1234859358945546314, 1224008543850463292, 1235518204512833569,
    1256598344873283726, 1256593718807625739, 1256595694030946325, 1256588043260006441,
    1279416527900246118, 1279416593733910600, 1279416598817669173, 1279416602156204052,
    1279416605494743070, 1279415950478807080, 1279416078870777878, 1279416101889114112,
    1279416108499341314, 1279416113419255839, 1279417317838815364, 1279417460600340511,
    1279417542980538409, 1279417609925689377, 1279417672362233876, 1279414710793535530, 
    1279415431244812318, 1279415509128839168, 1279415547909509130, 1279417999543242812, 
    1279418089124921425, 1279417470532194408, 1279417474521108520, 1279417477901848606,
    1270390997351927818, 1248312242827558932, 1261637379207204864, 1271369656040558655,
    1220350328247947275, 1176211427132973192, 1176211427132973191, 1176211427132973189,
    1286326488668307488, 1286326402165243927, 1286326442917101618, 1286326522122342400,
    1286326562802761820, 1286326588484489276, 1252972771453960333, 1176211427111997533,
    1286237500079079466, 1286237619818205184, 1286237658166595635, 1286237693017198613,
    1176211426709340208, 1176211426709340207, 1178265042228088862, 
    
]  # 삭제를 감지할 역할 ID
CHANNEL_IDS = [
    1289504633407934536, 1289505730574942259, 1286202271801278548, 1286202384057368616,
    1286202448070836264, 1286202334405459978, 1286202494678077490, 1286202530136850455,
    1286202557664071742, 1286214022332547103, 1286185252577873980, 1286172436781334579,
    1286395719510659093, 1286689771766284421, 1286689807187054612, 1286376720974221316,
    1286220758816915456, 1289517109205794877, 1286214700295520320, 1286226024706605098,
    1286220698360221758, 1286988969510436918, 1290580504403382292, 1286224389926289448,
    1296478547854098545, 1286226080180732006, 1178017101345214474, 1286212458310275094,
    1286212380216528949, 1286175664931733597, 1286212567986864190, 1286212686623014922,
    1286212755141165137, 1286212882664521731, 1288494404671246457, 1289548942299762698,
    1286212825123000340, 1178746941379710996, 1286213901691654155, 1286213000184991754,
    1286213172910358601, 1286216582598758451, 1179325123128475698, 1204087980156002314,
    1249344293987029032, 1275831640010133575, 1284824252650098763, 1296167096425775145,
    1296167123181109248, 1286867902112337920, 1287348462374879336, 1296059232864702514,
    1296113021961371798, 1296167070450319390, 1257936115105665064, 1272471652579541023,
    1290611649769639947, 1245731472934178816, 1286213814903242848, 1193916457906606150,
    1286213660720631809, 1286213685953695764, 1286213742220279810, 1286208729385009254,
    1286209137553965096, 1286208649399894056, 1286209259914395710, 1286209305682645012,
    1286208574401286187, 1286209218642444339, 1264940704916963349, 1229466042116341851,
    1286216418534227980, 1286211223553048627, 1286211334966611968, 1223995324880781312,
    1286219671506522163, 1224258360107466822, 1286208271677657099, 1286208082535251979,
    1286208131558281289, 1286208170750115860, 1286207975777898516, 1286207930512834601,
    1178258963440095314, 1178258983631454249, 1178259000362537000, 1177997987826372638,
    1286183190922395740, 1286183813621485702, 1286183918642397214, 1286207460109189130,
    1286207503293481012, 1286207546322980898, 1178018629061726258, 1189959320146817146,
    1190245898161246339, 1286207085226496071, 1286207153467555924, 1193776590983806986,
    1267404142867906613, 1267416861642068079, 1261898644613763183, 1286206575186280511,
    1286206609973972992, 1201427944845885440, 1178756026137329724, 1240690917623730208,
    1179888672456327349, 1208926352145915935, 1178281972771065956, 1294957775465746472,
    1286629102421540914, 1253026277607079988, 1253026940151926794, 1255572709740646503,
    1287056852160614420, 1294215015292862536, 1288489506009382952, 1178011973028425778,
    1178009950442766417, 1286206316087476285, 1286206359716761661, 1286205807607676951,
    1286205767338299445, 1202098870624981052, 1178012130067370034, 1178012198082191441,
    1178893892767207494, 1279407079370657793, 1178012280483495937, 1292863910780600362,
    1178010650375635036, 1178010707858571365, 1284452050553540678, 1178010790964502688,
    1178258808821264464, 1181450409940893716, 1178010820957962291, 1178009925612482621,
    1294590907483689041, 1286216903093911623, 1286216932101718016, 1286205012531478539,
    1178013480100565012, 1178060765916303400, 1178013462169931798, 1286205462408335432,
    1179891087314272316, 1179891189781110834, 1179891161385676898, 1179891313269821560,
    1202969376270061613, 1249011114243526699, 1286204118586621992, 1280178336441831508,
    1286259823100301333, 1179891810961727621, 1201530553002889216, 1190240974362914866,
    1191593523443671080, 1197561649914192002, 1297460035919544390 
]
ROLE_ID = 1176211427330109480  # 테러 시 알림을 받을 역할 ID -> 명월
REMOVE_ROLE_IDS = [1176211427330109479, 1176211427355267193] # 적월 은월

# 질문 목록과 답변 저장소
questions = {}
question_counter = 1
user_list = USER_LIST.split(",") if USER_LIST else []

# 실적 점수 저장할 딕셔너리
performance_scores = {user: 0 for user in user_list}
recommendation_counts = {user: 0 for user in user_list}
new_mention_counts = {user: 0 for user in user_list}

# 인텐트 설정
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
# 봇 초기화
bot = commands.Bot(command_prefix='.', intents=intents)

menu_dict = {
    "특식": ["불고기", "찜닭", "닭볶음탕", "제육볶음", "삼겹살", "오리불고기", "갈비찜", "낙지볶음", "오징어볶음", "소불고기"],
    "찌개": ["김치찌개", "된장찌개", "부대찌개", "순두부찌개", "고추장찌개", "동태찌개", "참치김치찌개", "청국장"],
    "덮밥/육류밥": ["카레", "오므라이스", "연어덮밥", "제육덮밥", "치킨마요덮밥", "장어덮밥", "불고기덮밥", "스팸덮밥"],
    "면": ["라면", "냉면", "짜장면", "짬뽕", "비빔국수", "칼국수", "우동", "쌀국수", "크림파스타", "토마토스파게티"],
    "해장": ["콩나물국밥", "북엇국", "순대국", "대파라면", "매운갈비탕", "뼈해장국", "소고기무국", "조개탕", "설렁탕"],
    "국/탕": ["갈비탕", "곰국", "순대국", "설렁탕", "닭곰탕", "육개장", "떡국", "추어탕", "알탕", "매운탕", "마라탕"],
    "기타": ["떡볶이", "샌드위치", "토스트", "핫도그", "핫케이크", "피자", "치킨", "소세지볶음", "프렌치토스트", "샐러드"],
}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.change_presence(activity=discord.Game(name="류 바보"), status=discord.Status.idle)

@bot.event
async def on_guild_channel_delete(channel):
    guild = channel.guild
    alert_role = guild.get_role(ROLE_ID)

    # 삭제를 수행한 사용자 확인
    async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
        user = entry.user
        user_roles = [role.id for role in user.roles]

        # 사용자의 역할이 REMOVE_ROLE_IDS에 있는지 확인
        if any(role_id in user_roles for role_id in REMOVE_ROLE_IDS):
            # 사용자 추방
            await guild.kick(user, reason=f"{channel.name} 채널 삭제로 인해 서버에서 추방됨")
            await send_alert(alert_role, f"{user.name}(이)가 '{channel.name}' 채널을 삭제하여 서버에서 추방되었습니다.")
            break

@bot.event
async def on_guild_role_delete(role):
    guild = role.guild
    alert_role = guild.get_role(ROLE_ID)

    # 삭제를 수행한 사용자 확인
    async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete):
        user = entry.user
        user_roles = [role.id for role in user.roles]

        # 사용자의 역할이 REMOVE_ROLE_IDS에 있는지 확인
        if any(role_id in user_roles for role_id in REMOVE_ROLE_IDS):
            # 사용자 추방
            await guild.kick(user, reason=f"{role.name} 역할 삭제로 인해 서버에서 추방됨")
            await send_alert(alert_role, f"{user.name}(이)가 '{role.name}' 역할을 삭제하여 서버에서 추방되었습니다.")
            break

@bot.event
async def on_guild_category_delete(category):
    guild = category.guild
    alert_role = guild.get_role(ROLE_ID)

    # 삭제를 수행한 사용자 확인
    async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
        user = entry.user
        user_roles = [role.id for role in user.roles]

        # 사용자의 역할이 REMOVE_ROLE_IDS에 있는지 확인
        if any(role_id in user_roles for role_id in REMOVE_ROLE_IDS):
            # 사용자 추방
            await guild.kick(user, reason=f"{category.name} 카테고리 삭제로 인해 서버에서 추방됨")
            await send_alert(alert_role, f"{user.name}(이)가 '{category.name}' 카테고리를 삭제하여 서버에서 추방되었습니다.")
            break

async def send_alert(alert_role, message):
    """알림을 받을 역할을 가진 모든 멤버에게 DM을 보내는 함수"""
    if alert_role:
        alert_tasks = [
            send_dm(member, message)
            for member in alert_role.members
        ]
        await asyncio.gather(*alert_tasks)

async def send_dm(member, message):
    """멤버에게 DM을 보내는 함수"""
    try:
        await member.send(message)
        print(f"Sent notification to {member.name}")
    except discord.Forbidden:
        print(f"Failed to send DM to {member.name} due to permissions.")
    except Exception as e:
        print(f"An error occurred while sending DM to {member.name}: {e}")

# 에스크봇 명령어들
@bot.command(name='에스크질문')
@commands.has_permissions(administrator=True)
async def create_question(ctx, *args):
    global question_counter
    question_text = ' '.join(args)
    question_id = question_counter
    question_counter += 1

    questions[question_id] = {
        "text": question_text,
        "answers": {user: "" for user in user_list}
    }

    user_answers = '\n\n'.join([f"{user} : " for user in user_list])
    await ctx.send(f"## 질문이 등록되었습니다!\n ### 질문 ID: {question_id}\n 질문 내용: {question_text}\n\n{user_answers}\n")
    
@bot.command(name='퇴근하고싶다')
async def time_until_off_work(ctx):
    now_utc = datetime.now(timezone.utc)  # UTC 시간 가져오기
    now_kst = now_utc + timedelta(hours=9)  # 한국 표준시(KST)로 변환
    end_time = now_kst.replace(hour=19, minute=0, second=0, microsecond=0)

    # 현재 시간이 퇴근 시간(오후 7시)을 넘겼을 경우, 다음 날 7시로 설정
    if now_kst > end_time:
        end_time += timedelta(days=1)

    remaining_time = end_time - now_kst
    hours, remainder = divmod(remaining_time.seconds, 3600)
    minutes = remainder // 60


    await ctx.send(f"퇴근시간까지 {hours}시간 {minutes}분 남았습니다.. 조금만 더 힘내!!!!!")

@bot.command(name='에스크답변')
async def answer_question(ctx, question_id: int, user_name: str, *response):
    if question_id not in questions:
        await ctx.send(f"존재하지 않는 질문 ID입니다: {question_id}")
        return

    if user_name not in questions[question_id]["answers"]:
        await ctx.send(f"'{user_name}' 유저에 대한 답변 항목이 없습니다.")
        return

    answer_text = ' '.join(response)
    questions[question_id]["answers"][user_name] = answer_text
    await ctx.send(f"{user_name} 님의 질문 ID {question_id}에 대한 답변이 등록되었습니다: {answer_text}")

@bot.command(name='에스크조회')
@commands.has_permissions(administrator=True)
async def view_question(ctx, question_id: int):
    if question_id not in questions:
        await ctx.send(f"존재하지 않는 질문 ID입니다: {question_id}")
        return

    question_data = questions[question_id]
    question_text = question_data["text"]
    answers = question_data["answers"]
    answers_text = '\n\n'.join([f"{user}: {response or '-'}" for user, response in answers.items()])
    await ctx.send(f"## 질문 ID {question_id}: {question_text}\n\n{answers_text}")

# 카테고리 메뉴 추천 함수
@bot.command(name='밥추천')
async def recommend_menu(ctx, category: str = None):
    """특정 카테고리 혹은 랜덤으로 밥 메뉴를 추천하는 명령어"""
    if category and category in menu_dict:
        recommended_menu = random.choice(menu_dict[category])
        await ctx.send(f"오늘의 메뉴는~~ **{category}** 카테고리에서 **{recommended_menu}** 먹으셈. 🍽️")
    elif not category:
        all_menus = sum(menu_dict.values(), [])
        recommended_menu = random.choice(all_menus)
        await ctx.send(f"오늘의 메뉴는~~ **{recommended_menu}** 먹으셈. 🍽️")
    else:
        await ctx.send(f"올바른 카테고리를 입력해주세요. 가능 카테고리: {', '.join(menu_dict.keys())}")
        
@bot.command(name='점메추')
async def jeom_menu_recommendation(ctx):
    await recommend_menu(ctx)

@bot.command(name='저메추')
async def jeo_menu_recommendation(ctx):
    await recommend_menu(ctx)

@bot.command(name='에스크도움말')
async def help_command(ctx):
    help_text = (
        "**📘 에스크봇 도움말**\n\n"
        "**📝 .에스크질문 [질문내용]** - 관리자 전용\n"
        "새로운 질문을 생성하고 유저들의 답변 목록을 초기화합니다.\n"
        "예시: `.에스크질문 짜장 vs 짬뽕`\n\n"
        "**💬 .에스크답변 [질문ID] [유저이름] [답변내용]**\n"
        "특정 질문 ID와 유저 이름에 대한 답변을 입력합니다.\n"
        "예시: `.에스크답변 1 주원 짜장`\n\n"
        "**🔍 .에스크조회 [질문ID]** - 관리자 전용\n"
        "특정 질문 ID에 대한 질문과 답변 목록을 조회합니다.\n"
        "예시: `.에스크조회 1`\n\n"
        "**❓ .에스크도움말**\n"
        "이 도움말을 표시합니다.\n"
        "예시: `.에스크도움말`"
    )
    await ctx.send(help_text)

# 활동 기록을 위한 행동 정의
actions = {
    "홍보10회": 100,
    "이름변경": 20,
    "등업": 20,
    "수집인증": 20,
    "건의함": 20,
    "뉴페멘션": 20,
    "조각지급": 50,
    "안내": 100,
    "역할구매": 100,
    "부스트편지": 100,
    "이벤트기획": 100,
    "경고내역": 100,
    "재입장": 100,
    "설야멘션": 100,
    "갠역멘션": 100,
    "면접참관": 200,
    "회의참여도": 200,
    "추천": 100,
    "초기화": 0
}

# 각 행동의 카운트를 저장하는 딕셔너리
action_counts = {action: 0 for action in actions.keys()}

@bot.command(name='실적')
async def performance_command(ctx, user_name: str, action: str):
    """유저 이름과 행동을 기반으로 실적 점수를 조정하는 명령어"""
    await manage_performance(ctx, user_name, action)

async def manage_performance(ctx, user_name: str, action: str):
    if user_name not in user_list:
        await ctx.send(f"{user_name}은(는) 유효한 유저가 아닙니다. 다음 유저들 중에서 선택해주세요: {', '.join(user_list)}")
        return

    if action == "초기화":
        performance_scores[user_name] = 0
        action_counts[user_name] = {action: 0 for action in actions.keys()}  # 초기화 시 행동 카운트 리셋
        await ctx.send(f"'{user_name}' 님의 실적이 초기화되었습니다.")
        return

    if action not in actions:
        await ctx.send(f"올바른 명령어를 사용해주세요. 사용 가능한 명령어: {', '.join(actions.keys())} 및 초기화")
        return

    # 행동 카운트 증가
    action_counts[action] += 1

    # 특정 액션에 따라 점수 증가 처리
    if action == "추천":
        recommendation_counts[user_name] = recommendation_counts.get(user_name, 0) + 1
        if recommendation_counts[user_name] == 7:
            await update_performance(user_name, actions["추천"])
            await ctx.send(f"{user_name}의 추천이 7회 누적되어 100점이 추가되었습니다.")
        else:
            await ctx.send(f"{user_name}의 추천 횟수가 {recommendation_counts[user_name]}회 누적되었습니다. (7회 시 100점 추가)")
        new_mention_counts[user_name] = new_mention_counts.get(user_name, 0) + 1
    else:
        await update_performance(user_name, actions[action])
        await ctx.send(f"'{user_name}' 님의 실적이 {actions[action]}점 증가했습니다.")

async def update_performance(user_name: str, points: int):
    """특정 유저의 실적 점수를 업데이트하는 함수"""
    performance_scores[user_name] += points

@bot.command(name='실적초기화')
async def performance_reset(ctx, user_name: str):
    """유저 이름을 받아 해당 유저의 실적 점수를 초기화하는 명령어"""
    if user_name not in user_list:
        await ctx.send(f"{user_name}은(는) 유효한 유저가 아닙니다. 다음 유저들 중에서 선택해주세요: {', '.join(user_list)}")
        return

    await manage_performance(ctx, user_name, '초기화')
    
@bot.command(name='실적조회')
async def total_performance(ctx, user_name: str):
    """유저 이름을 받아 해당 유저의 총 실적 점수를 조회하는 명령어"""
    if user_name not in user_list:
        await ctx.send(f"{user_name}은(는) 유효한 유저가 아닙니다. 다음 유저들 중에서 선택해주세요: {', '.join(user_list)}")
        return

    total_points = performance_scores.get(user_name, 0)
    await ctx.send(f"'{user_name}' 님의 총 실적 점수는 {total_points}점입니다.")
    
@bot.command(name='야옹')
async def 현하_command(ctx):
    """ '.현하' 명령어를 입력하면 # 바보 형식으로 큰 글씨로 응답 """
    await ctx.send("# 애기")  
    
@bot.command(name='메리')
async def 현하_command(ctx):
    """ '.현하' 명령어를 입력하면 # 바보 형식으로 큰 글씨로 응답 """
    await ctx.send("미 || 뭐 현하야 결혼하자고?")  
        
@bot.command(name='여은')
async def 현하_command(ctx):
    """ '.현하' 명령어를 입력하면 # 바보 형식으로 큰 글씨로 응답 """
    await ctx.send("# 공주")  

@bot.command(name='실적도움말')
async def help_command(ctx):
    """사용 가능한 명령어에 대한 도움말을 제공하는 명령어"""
    help_text = (
        "**사용 가능한 명령어:**\n"
        "- 📜 `.실적 <유저 이름> <실적>`: 실적을 등록합니다.\n"
        "   - **실적 예시:** `홍보10회`, `이름변경`, `등업`, `수집인증` 등\n"
        "- 🔍 `.실적조회 <유저 이름>`: 유저의 실적을 조회합니다.\n"
        "- 🔄 `.실적초기화 <유저 이름>`: 유저의 실적 점수를 초기화합니다.\n"
        "- ❓ `.실적도움말`: 사용 가능한 명령어를 확인합니다.\n"
    )
    await ctx.send(help_text)

@bot.command(name='반속제한')
@commands.has_permissions(administrator=True)  # 관리자 권한 체크
async def block_chat(ctx):
    role_id = 1286174278227722240  # 채팅을 제한할 역할 ID
    role = ctx.guild.get_role(role_id)

    if role is None:
        await ctx.send("지정된 역할을 찾을 수 없습니다.")
        return

    # 현재 채널에서 해당 역할의 기존 권한을 가져옴
    current_overwrites = ctx.channel.overwrites_for(role)

    # 메시지 보내기 권한만 False로 변경 (다른 권한은 유지)
    current_overwrites.send_messages = False
    await ctx.channel.set_permissions(role, overwrite=current_overwrites)
    await ctx.send(f"{role.name} 역할이 3초 동안 채팅을 할 수 없습니다.")

    # 3초 후 다시 메시지 보내기 권한을 원래대로 복구
    await asyncio.sleep(3)
    current_overwrites.send_messages = None  # 원래 상태로 복구 (기본 권한)
    await ctx.channel.set_permissions(role, overwrite=current_overwrites)
    await ctx.send(f"{role.name} 역할이 다시 채팅을 할 수 있습니다.")

# 관리자 권한이 없는 사용자가 명령어를 사용할 때 에러 처리
@block_chat.error
async def block_chat_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("이 명령어를 사용하려면 관리자 권한이 필요합니다.")
        
        # Heroku sleep 방지용 메시지 전송 함수
def send_heartbeat_message():
    channel_id = 1301052135143899137  # 메시지를 보낼 임의의 채널 ID로 바꾸세요
    channel = bot.get_channel(channel_id)
    if channel:
        message = random.choice(["설탕이 sleep 모드 방지 메시지"])
        asyncio.run_coroutine_threadsafe(channel.send(message), bot.loop)

# 29분마다 실행될 스케줄러 설정
def schedule_heartbeat():
    schedule.every(29).minutes.do(send_heartbeat_message)

    while True:
        schedule.run_pending()
        time.sleep(1)

# 봇 이벤트: 봇이 준비되었을 때 스케줄러 시작
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    # 새로운 스레드에서 스케줄러 실행
    threading.Thread(target=schedule_heartbeat).start()

@bot.command(name='역할유저')
@commands.has_permissions(administrator=True)  # 관리자 권한 체크
async def get_users_with_role(ctx, role_id: int, *, new_prefix: str):
    """특정 역할을 가진 유저 중 '【 낙화 】'로 시작하는 유저의 닉네임을 변경하는 명령어"""
    role = ctx.guild.get_role(role_id)
    
    if role is None:
        await ctx.send(f"ID가 {role_id}인 역할을 찾을 수 없습니다.")
        return

    members_with_role = [member for member in ctx.guild.members if role in member.roles]
    
    if not members_with_role:
        await ctx.send(f"{role.name} 역할을 가진 유저가 없습니다.")
        return
    
    # 닉네임이 "【 낙화 】"로 시작하는 유저만 필터링
    members_to_update = [member for member in members_with_role if member.display_name.startswith("【 낙화 】")]

    if not members_to_update:
        await ctx.send(f"'【 낙화 】'로 시작하는 닉네임을 가진 유저가 없습니다.")
        return
    
    # 닉네임 변경
    for i, member in enumerate(members_to_update):
        new_nickname = member.display_name.replace("【 낙화 】", f"【 {new_prefix} 】")
        try:
            await member.edit(nick=new_nickname)
            await ctx.send(f"{member.display_name}의 닉네임이 '{new_nickname}'으로 변경되었습니다.")
        except discord.Forbidden:
            await ctx.send(f"{member.display_name}의 닉네임을 변경할 수 없습니다. 권한이 없습니다.")
        except discord.HTTPException:
            await ctx.send(f"{member.display_name}의 닉네임 변경 중 오류가 발생했습니다.")
    
    await ctx.send(f"'【 낙화 】'로 시작하는 유저들의 닉네임을 '【 {new_prefix} 】'로 변경했습니다.")


# 봇 실행
bot.run(TOKEN)
