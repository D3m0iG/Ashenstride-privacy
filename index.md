# Ashenstride — Privacy Policy / Política de privacidade

*[English](#english) · [Português](#português-pt-pt)*

---

## English

**Last updated:** 17 November 2026  
**Developer / controller:** Luis Barros (individual developer, Portugal) — contact: **luis.baf0z@gmail.com**

**Summary.** Ashenstride has no ads and no usage analytics, and you can play all of it without any account. Your progress and your steps stay on your phone. The game sends **anonymous crash and freeze reports** (Firebase Crashlytics, Google) so we can fix problems quickly; this is **on by default and you can switch it off at any time** in Settings → Data. Only if you turn on the optional "Cloud save" feature (by signing in with Google Play Games; off by default), the game uploads a copy of your game save to **your own Google account** through Google Play Games, so you can restore it on another phone. Only if you choose to use the optional **Friends** feature, the game creates a player account for you and keeps a small profile on our server (nickname, level, avatar, friend code and your friends list; see section 3b); you can delete it at any time. If you buy the optional in-game item, Google Play handles the payment. We, the developer, do not receive, see or store the cloud copy or your payment details, and we do not sell any of your data.

### 1. What the app does on your phone
- **Steps.** Read from Android's activity sensor ("Physical activity" permission) and, when available, from Health Connect (permission to **read** steps only; the app never writes to Health Connect). Steps become in-game progress (travel, encounters, rewards). They are processed **only on your phone** and are never sent anywhere.
- **Background step reading.** If you turn on phone alerts, the app periodically reads aggregated steps from Health Connect even when the game is closed, only to notify you when your hero arrives somewhere. You can turn it off in Settings → "Phone alerts".
- **Notifications** (with your permission; quiet hours 10 pm–8 am by default) and **vibration** (can be turned off in Settings).
- **Game data** (progress, inventory, settings) is stored in the app's private storage on your phone.

### 2. Backups of your progress
- **Android backup (Google).** Android may back up the game's saved data to **your own Google account** (Google Drive) so it can be restored on a new phone. This is done by Android and Google, under your Google account settings and Google's privacy policy; the developer does not receive or have access to it. You can turn it off in your phone's Google backup settings.
- **Export / import.** In Settings → Data you can export your progress to a file that **you** choose where to save, and import it on another phone. The file only goes where you put it.
- **Cloud save (optional, off by default).** If you tap **"Sign in with Google Play Games"** (on the first screen of the game or in Settings → Google Play account), the game signs you in to **Google Play Games** and uploads a copy of your game save for each character to your Google account (Play Games "Saved Games"). The copy contains your character's progress (level, inventory, map and story progress) and the game's own step counters (how many steps the game has counted, and the technical data the game keeps to avoid counting the same steps twice, which can include the names of the apps that supplied your steps through Health Connect). It does not contain your location, contacts or the raw Health Connect records. The copy is sent over an encrypted connection (HTTPS) and is stored and processed by Google under your Google account settings and Google's privacy policy; the developer has no access to it. Only the campaign you play for real is uploaded. While you are signed in, the game shows your Play Games gamer name on the screen; the game does not store it or send it anywhere. After you sign in once, the game signs in again by itself every time you open it, until you tap **"Sign out"** (on the first screen or in Settings → Google Play account). You can sign out at any time (this stops new uploads; the existing copy stays until you delete it) and you can delete the cloud copy in Settings → Data → "Delete cloud copy", in the Google Play Games app, or in your Google Account. Google Play Games may also collect diagnostics and analytics for its own service, as described in Google's documentation. The game only starts this once you turn the feature on.

### 3. Internet, purchases and third parties
The app uses the Internet **only** for (a) anonymous crash and freeze reports (see section 3a), (b) the optional cloud save described above, and only after you turn it on, (c) the optional purchase of the in-game item (diamonds) through **Google Play Billing**, and (d) the optional Friends feature (section 3b), and only after you enter it. Payments are processed entirely by Google Play, under Google's terms and privacy policy; the developer does not receive your card or payment details, only the confirmation that a purchase was made. The app does not contain advertising or usage analytics. The only third party involved is Google (Firebase Crashlytics, Firebase Authentication and Cloud Firestore, Google Play Games Services and Google Play Billing). Nothing else is sent to the developer.

### 3a. Anonymous crash and freeze reports (Firebase Crashlytics)
**On by default.** To fix crashes and freezes quickly, the app sends anonymous crash and freeze reports to **Firebase Crashlytics (Google)** as soon as they happen. You can switch this off at any time in **Settings → Data → "Send anonymous crash reports"**; after that nothing more is sent. The game tells you about this the first time you open it.
- **What is sent:** the technical error (where in the code it failed), how long a freeze lasted and on which screen, the game version, your phone model, the Android version, the memory state at the time of the failure, and an installation identifier generated by Firebase (it does not identify you personally).
- **What the game never puts in a report:** your name, e-mail, Google Play Games ID, location, step counts, progress, inventory or save files.
- **Who receives it:** Google acts as our service provider (processor) for this. See https://firebase.google.com/support/privacy. Because a report is an ordinary Internet request, Google's servers see your IP address in the process; the game does not add it to the report.
- **Why (legal basis):** our legitimate interest in keeping the game stable, with an easy switch-off.

### 3b. Friends (optional)
The game works completely without this. Nothing described here happens until you open **Settings → Friends** and tap **"Enter friends"**.
- **Player account.** When you enter, the game signs you in to **Firebase Authentication (Google)** with your Google Play Games profile. This creates a player account with an identifier generated by Firebase. Google keeps with it your Play Games player ID and the public Play Games profile that Google supplies at sign-in (your gamer name and the address of your profile picture), the dates of creation and of your last sign-in and, for security, the IP address used. The game does not receive your e-mail address.
- **Protection against abuse.** While you use Friends, the game asks **Firebase App Check with Google Play Integrity (Google)** to confirm that its requests come from the genuine game, installed from Google Play, on a genuine device. To do this, Google receives technical information about the app and the device. We do not receive that information: the game only gets a short-lived proof that the check passed, which it attaches to its requests.
- **Profile.** Only if you then choose to create a profile, we store in **Cloud Firestore (Google, servers in the European Union)**: the **nickname** you choose (up to 24 characters), your hero's **level**, an **avatar** (one of 12 colours), a random **friend code**, and the date of the last change.
- **Friends, requests, blocks and gifts.** We store who your friends are and since when, friend requests you sent or received that are still waiting, the players you blocked, and gifts waiting to be collected (who gave them and on which day).
- **Who can see what.** Your friends, people you sent a request to or who sent you one, and anyone you give your friend code to can see your nickname, level and avatar. Nobody can browse or search the list of players: a profile can only be opened with its exact code. Your steps, location, e-mail and game progress are never part of the profile.
- **Reports.** If a player reports another one, we store who reported, who was reported, the reason chosen from a fixed list, the day and the nickname the reported player had at that moment. Only the developer can read reports, and uses them only to moderate (for example to remove an offensive nickname or to close an account). Reports are kept for up to 12 months.
- **There is no chat.** Players cannot write messages to each other; the only free text is the nickname.
- **How long.** Until you delete it. **Settings → Friends → "Delete my social data…"** deletes your profile, friend code, friendships, requests, unclaimed gifts, blocks and the player account itself. Reports are the exception described above.
- **Who processes it:** Google, as our service provider (processor). See https://firebase.google.com/support/privacy.
- **Why (legal basis):** your consent, which you give by entering the feature and creating a profile, and which you withdraw by deleting your data.

### 4. E-mail
If you write to luis.baf0z@gmail.com, we receive your e-mail address and whatever you write, and we use them only to answer you.

### 5. Your choices and rights
- Uninstalling the app, or Android Settings → Apps → Ashenstride → Storage → "Clear data", removes everything stored on your phone by the app. A cloud copy, if you made one, stays in your Google account until you delete it (Settings → Data → "Delete cloud copy", the Google Play Games app, or your Google Account).
- You can revoke the step and notification permissions at any time in Android or Health Connect settings.
- Unless you use the optional Friends feature, the developer holds no personal data about you (crash reports are anonymous and held by Google as our service provider), so there is nothing for us to delete, correct or export; for the cloud copy use the options above. If you use Friends, you can see and change your profile in Settings → Friends, delete everything there, or ask us by e-mail for a copy or for deletion (tell us your friend code). If you believe we hold data about you (for example from an e-mail you sent), write to us and we will answer. You may also complain to your data-protection authority (in Portugal: CNPD, cnpd.pt).

### Delete your data (Ashenstride, by Luis Barros)
Full instructions, including how to ask for deletion without the app: **[Delete your data](apagar-dados)**.

**Friends data and player account (only if you used the optional Friends feature).** In the game: **Settings → Friends → "Delete my social data…"**. This deletes your profile, friend code, friendships, requests, unclaimed gifts, blocks and your player account. If you no longer have the game, write to luis.baf0z@gmail.com with your friend code and we delete it within 30 days.

**Cloud copy.** Apart from that, the only data that can exist outside your phone is the optional **cloud copy** of your game save in **your own Google account**. To delete it:
1. In the game: **Settings → Data → "Delete cloud copy"**; or
2. In the **Google Play Games** app: your profile → Settings → "Delete Play Games account and data" (choose Ashenstride); or
3. In your **Google Account** (myaccount.google.com → Data & privacy → Third-party apps and services → Ashenstride).
To remove everything stored on your phone, uninstall the app or use Android Settings → Apps → Ashenstride → Storage → "Clear data". You can also ask by e-mail (luis.baf0z@gmail.com) and we will help you.

### 6. Permissions
Physical activity (step sensor), Health Connect steps (read only), notifications, vibration and **Internet (only for anonymous crash reports, the optional cloud save, the optional Friends feature and purchases through Google Play)**. The app has no location, contacts, camera, microphone or storage permission.

### 7. Children
The app is not directed at children under 13. The optional Friends feature has no chat; the only text other players can see is the nickname, which can be reported and blocked.

### 8. Changes
If this policy changes, the date above will be updated.

---

## Português (PT-PT)

**Última atualização:** 17 de novembro de 2026  
**Programador / responsável:** Luis Barros (programador individual, Portugal) — contacto: **luis.baf0z@gmail.com**

**Resumo.** O Ashenstride não tem anúncios nem estatísticas de utilização, e podes jogá-lo todo sem conta nenhuma. O teu progresso e os teus passos ficam no teu telemóvel. O jogo envia **relatórios anónimos de falhas e bloqueios** (Firebase Crashlytics, da Google) para podermos corrigir problemas depressa; isto está **ligado por defeito e podes desligar a qualquer momento** em Definições → Dados. Só se ligares a função opcional «Cópia na nuvem» (ao entrares com o Google Play Jogos; desligada por defeito), o jogo envia uma cópia do teu save para **a tua própria conta Google**, através do Google Play Games, para a poderes recuperar noutro telemóvel. Só se escolheres usar a função opcional **Amigos**, o jogo cria-te uma conta de jogador e guarda no nosso servidor um perfil pequeno (alcunha, nível, avatar, código de amigo e a tua lista de amigos; ver secção 3b); podes apagá-lo a qualquer momento. Se comprares o item opcional do jogo, é a Google Play que trata do pagamento. Nós, o programador, não recebemos, não vemos nem guardamos a cópia na nuvem nem os teus dados de pagamento, e não vendemos nenhum dado teu.

### 1. O que a app faz no teu telemóvel
- **Passos.** Lidos do sensor de atividade do Android (permissão «Atividade física») e, quando existe, do Health Connect (permissão só para **ler** passos; a app nunca escreve no Health Connect). Os passos transformam-se em progresso no jogo (viagem, encontros, recompensas). São tratados **apenas no teu telemóvel** e nunca são enviados para lado nenhum.
- **Leitura de passos em segundo plano.** Se ativares os alertas do telemóvel, a app lê periodicamente os passos agregados do Health Connect mesmo com o jogo fechado, só para te avisar quando o teu herói chega a um sítio. Podes desligar em Definições → «Alertas do telemóvel».
- **Notificações** (com a tua permissão; horas de silêncio das 22h às 8h por defeito) e **vibração** (pode ser desligada nas Definições).
- **Dados do jogo** (progresso, inventário, definições) ficam no armazenamento privado da app, no teu telemóvel.

### 2. Cópias de segurança do progresso
- **Backup do Android (Google).** O Android pode guardar uma cópia dos dados do jogo na **tua própria conta Google** (Google Drive), para os repor num telemóvel novo. É feito pelo Android e pela Google, segundo as definições da tua conta Google e a política de privacidade da Google; o programador não recebe nem tem acesso a essa cópia. Podes desligá-lo nas definições de backup Google do teu telemóvel.
- **Exportar / importar.** Em Definições → Dados podes exportar o teu progresso para um ficheiro, que **tu** escolhes onde guardar, e importá-lo noutro telemóvel. O ficheiro só vai para onde o puseres.
- **Cópia na nuvem (opcional, desligada por defeito).** Se carregares em **«Entrar com Google Play Jogos»** (no primeiro ecrã do jogo ou em Definições → Conta Google Play), o jogo inicia sessão no **Google Play Games** e envia para a tua conta Google uma cópia do save de cada personagem (os «Jogos guardados» do Play Games). A cópia contém o progresso da personagem (nível, inventário, progresso no mapa e na história) e os contadores de passos do próprio jogo (quantos passos o jogo já contou e os dados técnicos que o jogo guarda para não contar os mesmos passos duas vezes, que podem incluir os nomes das aplicações que forneceram os teus passos através do Health Connect). Não contém a tua localização, contactos nem os registos em bruto do Health Connect. A cópia é enviada por ligação cifrada (HTTPS) e é guardada e tratada pela Google, segundo as definições da tua conta Google e a política de privacidade da Google; o programador não tem acesso. Só é enviada a campanha que jogas a sério. Enquanto tiveres a sessão iniciada, o jogo mostra no ecrã o teu nome de jogador do Play Games; o jogo não o guarda nem o envia para lado nenhum. Depois de entrares uma vez, o jogo volta a entrar sozinho sempre que o abres, até carregares em **«Sair»** (no primeiro ecrã ou em Definições → Conta Google Play). Podes sair a qualquer momento (isso pára os novos envios; a cópia existente fica até a apagares) e podes apagar a cópia na nuvem em Definições → Dados → «Apagar cópia da nuvem», na app Google Play Games ou na tua Conta Google. O Google Play Games pode também recolher dados de diagnóstico e de utilização para o seu próprio serviço, como a Google descreve na sua documentação. O jogo só inicia isto depois de ligares a função.

### 3. Internet, compras e terceiros
A app usa a Internet **apenas** para (a) relatórios anónimos de falhas e bloqueios (ver secção 3a), (b) a cópia opcional na nuvem descrita acima, e só depois de a ligares, (c) a compra opcional do item do jogo (diamantes) através do **Google Play Billing**, e (d) a função opcional Amigos (secção 3b), e só depois de entrares nela. Os pagamentos são tratados inteiramente pela Google Play, segundo os termos e a política de privacidade da Google; o programador não recebe os dados do teu cartão ou de pagamento, só a confirmação de que houve uma compra. A app não contém publicidade nem estatísticas de utilização. O único terceiro envolvido é a Google (Firebase Crashlytics, Firebase Authentication e Cloud Firestore, Google Play Games Services e Google Play Billing). Mais nada é enviado ao programador.

### 3a. Relatórios anónimos de falhas e bloqueios (Firebase Crashlytics)
**Ligado por defeito.** Para corrigir falhas e bloqueios depressa, a app envia relatórios anónimos de falhas e bloqueios para o **Firebase Crashlytics (Google)** assim que acontecem. Podes desligar a qualquer momento em **Definições → Dados → «Enviar relatórios de falhas anónimos»**; depois disso não é enviado mais nada. O jogo avisa-te disto na primeira vez que o abres.
- **O que é enviado:** o erro técnico (em que parte do código falhou), quanto durou um bloqueio e em que ecrã, a versão do jogo, o modelo do telemóvel, a versão do Android, o estado da memória no momento da falha e um identificador de instalação gerado pelo Firebase (não te identifica pessoalmente).
- **O que o jogo nunca põe num relatório:** o teu nome, e-mail, ID do Google Play Games, localização, passos, progresso, inventário ou saves.
- **Quem recebe:** a Google, como prestador de serviços do programador. Ver https://firebase.google.com/support/privacy. Como um relatório é um pedido normal de Internet, os servidores da Google veem o teu endereço IP; o jogo não o junta ao relatório.
- **Porquê (base legal):** o nosso interesse legítimo em manter o jogo estável, com um interruptor fácil para desligar.

### 3b. Amigos (opcional)
O jogo funciona todo sem isto. Nada do que aqui se descreve acontece até abrires **Definições → Amigos** e carregares em **«Entrar nos amigos»**.
- **Conta de jogador.** Ao entrar, o jogo inicia sessão no **Firebase Authentication (Google)** com o teu perfil do Google Play Games. Isto cria uma conta de jogador com um identificador gerado pelo Firebase. A Google guarda com ela o teu ID de jogador do Play Games e o perfil público do Play Games que a Google fornece no início de sessão (o teu nome de jogador e o endereço da tua imagem de perfil), as datas de criação e do último início de sessão e, por segurança, o endereço IP usado. O jogo não recebe o teu endereço de e-mail.
- **Proteção contra abusos.** Enquanto usas os Amigos, o jogo pede ao **Firebase App Check com o Google Play Integrity (Google)** que confirme que os pedidos vêm do jogo verdadeiro, instalado pelo Google Play, num dispositivo verdadeiro. Para isso, a Google recebe informação técnica sobre a app e o dispositivo. Nós não recebemos essa informação: o jogo recebe apenas uma prova de curta duração de que a verificação passou, que junta aos seus pedidos.
- **Perfil.** Só se depois escolheres criar um perfil, guardamos no **Cloud Firestore (Google, servidores na União Europeia)**: a **alcunha** que escolheres (até 24 caracteres), o **nível** do teu herói, um **avatar** (uma de 12 cores), um **código de amigo** aleatório e a data da última alteração.
- **Amigos, pedidos, bloqueios e presentes.** Guardamos quem são os teus amigos e desde quando, os pedidos de amizade que enviaste ou recebeste e ainda esperam resposta, os jogadores que bloqueaste e os presentes por apanhar (quem os deu e em que dia).
- **Quem vê o quê.** Os teus amigos, as pessoas a quem enviaste um pedido ou que to enviaram, e quem tiver o teu código de amigo vêem a tua alcunha, o teu nível e o teu avatar. Ninguém consegue percorrer nem pesquisar a lista de jogadores: um perfil só se abre com o código exato. Os teus passos, a tua localização, o teu e-mail e o teu progresso no jogo nunca fazem parte do perfil.
- **Denúncias.** Se um jogador denunciar outro, guardamos quem denunciou, quem foi denunciado, o motivo escolhido de uma lista fixa, o dia e a alcunha que o denunciado tinha nesse momento. Só o programador lê as denúncias, e usa-as apenas para moderar (por exemplo, retirar uma alcunha ofensiva ou fechar uma conta). As denúncias são guardadas até 12 meses.
- **Não há conversas.** Os jogadores não podem escrever mensagens uns aos outros; o único texto livre é a alcunha.
- **Durante quanto tempo.** Até apagares. **Definições → Amigos → «Apagar os meus dados sociais…»** apaga o teu perfil, o código de amigo, as amizades, os pedidos, os presentes por apanhar, os bloqueios e a própria conta de jogador. As denúncias são a exceção descrita acima.
- **Quem trata:** a Google, como prestador de serviços do programador. Ver https://firebase.google.com/support/privacy.
- **Porquê (base legal):** o teu consentimento, que dás ao entrar na função e criar um perfil, e que retiras ao apagar os teus dados.

### 4. E-mail
Se escreveres para luis.baf0z@gmail.com, recebemos o teu endereço de e-mail e o que escreveres, e usamo-los apenas para te responder.

### 5. As tuas escolhas e direitos
- Desinstalar a app, ou Definições do Android → Aplicações → Ashenstride → Armazenamento → «Limpar dados», remove tudo o que a app guardou no teu telemóvel. Uma cópia na nuvem, se a fizeste, fica na tua conta Google até a apagares (Definições → Dados → «Apagar cópia da nuvem», app Google Play Games ou Conta Google).
- Podes retirar as permissões de passos e notificações a qualquer momento nas definições do Android ou do Health Connect.
- Se não usares a função opcional Amigos, o programador não tem dados pessoais teus (os relatórios de falhas são anónimos e ficam na Google, como nosso prestador de serviços), por isso não há nada para apagar, corrigir ou exportar; para a cópia na nuvem usa as opções acima. Se usares os Amigos, podes ver e mudar o teu perfil em Definições → Amigos, apagar tudo aí mesmo, ou pedir-nos por e-mail uma cópia ou a eliminação (diz-nos o teu código de amigo). Se achares que temos dados teus (por exemplo, de um e-mail que enviaste), escreve-nos e respondemos. Podes também apresentar queixa à autoridade de proteção de dados (em Portugal: CNPD, cnpd.pt).

### Apagar os teus dados (Ashenstride, de Luis Barros)
Instruções completas, incluindo como pedir a eliminação sem a app: **[Apagar os teus dados](apagar-dados)**.

**Dados dos amigos e conta de jogador (só se usaste a função opcional Amigos).** No jogo: **Definições → Amigos → «Apagar os meus dados sociais…»**. Isto apaga o teu perfil, o código de amigo, as amizades, os pedidos, os presentes por apanhar, os bloqueios e a tua conta de jogador. Se já não tiveres o jogo, escreve para luis.baf0z@gmail.com com o teu código de amigo e apagamos tudo no prazo de 30 dias.

**Cópia na nuvem.** Fora isso, os únicos dados que podem existir fora do teu telemóvel são a **cópia opcional na nuvem** do teu save, na **tua própria conta Google**. Para a apagar:
1. No jogo: **Definições → Dados → «Apagar cópia da nuvem»**; ou
2. Na app **Google Play Games**: o teu perfil → Definições → «Eliminar conta e dados do Play Games» (escolhe o Ashenstride); ou
3. Na tua **Conta Google** (myaccount.google.com → Dados e privacidade → Apps e serviços de terceiros → Ashenstride).
Para remover tudo o que está no teu telemóvel, desinstala a app ou usa Definições do Android → Aplicações → Ashenstride → Armazenamento → «Limpar dados». Também podes pedir por e-mail (luis.baf0z@gmail.com) e ajudamos-te.

### 6. Permissões
Atividade física (sensor de passos), passos do Health Connect (só leitura), notificações, vibração e **Internet (só para os relatórios anónimos de falhas, a cópia opcional na nuvem, a função opcional Amigos e as compras através da Google Play)**. A app não tem permissão de localização, contactos, câmara, microfone nem armazenamento.

### 7. Crianças
A app não se destina a crianças com menos de 13 anos. A função opcional Amigos não tem conversas; o único texto que os outros jogadores vêem é a alcunha, que pode ser denunciada e bloqueada.

### 8. Alterações
Se esta política mudar, a data acima será atualizada.
