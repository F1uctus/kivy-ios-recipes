/*
 SpacySmoke — minimal UIKit host for kivy-ios embedded CPython + spaCy smoke.py
 Build on macOS with XcodeGen (see BUILD.md).
 */

#import <UIKit/UIKit.h>
#include <Python.h>

@interface SpacySmokeVC : UIViewController
@property (nonatomic, strong) UITextView *textView;
@property (nonatomic, copy) NSString *lastLogPath;
@end

@implementation SpacySmokeVC

- (void)viewDidLoad {
  [super viewDidLoad];
  self.view.backgroundColor = [UIColor systemBackgroundColor];
  self.title = @"Spacy smoke";

  UIButton *btnRun = [UIButton buttonWithType:UIButtonTypeSystem];
  [btnRun setTitle:@"Run smoke.py" forState:UIControlStateNormal];
  btnRun.translatesAutoresizingMaskIntoConstraints = NO;
  [btnRun addTarget:self action:@selector(onRun) forControlEvents:UIControlEventTouchUpInside];

  UIButton *btnCopy = [UIButton buttonWithType:UIButtonTypeSystem];
  [btnCopy setTitle:@"Copy all" forState:UIControlStateNormal];
  btnCopy.translatesAutoresizingMaskIntoConstraints = NO;
  [btnCopy addTarget:self action:@selector(onCopy) forControlEvents:UIControlEventTouchUpInside];

  UIButton *btnShare = [UIButton buttonWithType:UIButtonTypeSystem];
  [btnShare setTitle:@"Share log file" forState:UIControlStateNormal];
  btnShare.translatesAutoresizingMaskIntoConstraints = NO;
  [btnShare addTarget:self action:@selector(onShare) forControlEvents:UIControlEventTouchUpInside];

  UIStackView *bar = [[UIStackView alloc] initWithArrangedSubviews:@[ btnRun, btnCopy, btnShare ]];
  bar.axis = UILayoutConstraintAxisHorizontal;
  bar.distribution = UIStackViewDistributionFillEqually;
  bar.spacing = 8;
  bar.translatesAutoresizingMaskIntoConstraints = NO;

  self.textView = [[UITextView alloc] initWithFrame:CGRectZero];
  self.textView.translatesAutoresizingMaskIntoConstraints = NO;
  self.textView.font = [UIFont monospacedSystemFontOfSize:12 weight:UIFontWeightRegular];
  self.textView.editable = NO;
  self.textView.text = @"Tap “Run smoke.py”. Full trace is written under Documents/spacy_smoke_log.txt\n"
                         @"Use “Copy all” or “Share log file” to send output.\n";

  [self.view addSubview:bar];
  [self.view addSubview:self.textView];

  UILayoutGuide *safe = self.view.safeAreaLayoutGuide;
  [NSLayoutConstraint activateConstraints:@[
    [bar.topAnchor constraintEqualToAnchor:safe.topAnchor constant:8],
    [bar.leadingAnchor constraintEqualToAnchor:safe.leadingAnchor constant:12],
    [bar.trailingAnchor constraintEqualToAnchor:safe.trailingAnchor constant:-12],

    [self.textView.topAnchor constraintEqualToAnchor:bar.bottomAnchor constant:12],
    [self.textView.leadingAnchor constraintEqualToAnchor:safe.leadingAnchor constant:8],
    [self.textView.trailingAnchor constraintEqualToAnchor:safe.trailingAnchor constant:-8],
    [self.textView.bottomAnchor constraintEqualToAnchor:safe.bottomAnchor constant:-8],
  ]];
}

static NSString *RunEmbeddedPython(NSArray<NSString *> *docPaths, NSString *resPath, NSString *smokePath) {
  NSMutableString *out = [NSMutableString string];

  if (docPaths.count == 0)
    return @"No Documents directory.";
  NSString *docs = docPaths[0];

  setenv("PYTHONDONTWRITEBYTECODE", "1", 1);
  setenv("PYTHONUNBUFFERED", "1", 1);
  setenv("PYTHONNOUSERSITE", "1", 1);
  setenv("IOS_APP_DOCUMENTS", docs.UTF8String, 1);

  NSString *pythonHome = [resPath stringByAppendingPathComponent:@"python3"];
  setenv("PYTHONHOME", pythonHome.UTF8String, 1);

  NSString *site = [pythonHome stringByAppendingPathComponent:@"lib/python3.13/site-packages"];
  NSString *pypath = [NSString stringWithFormat:@"%@:%@", site, pythonHome];
  setenv("PYTHONPATH", pypath.UTF8String, 1);

  NSString *tmp = [docs stringByAppendingPathComponent:@"python_tmp"];
  [[NSFileManager defaultManager] createDirectoryAtPath:tmp withIntermediateDirectories:YES attributes:nil error:nil];
  setenv("TMPDIR", tmp.UTF8String, 1);

  [out appendFormat:@"[objc] PYTHONHOME=%s\n", getenv("PYTHONHOME")];
  [out appendFormat:@"[objc] PYTHONPATH=%s\n", getenv("PYTHONPATH")];
  [out appendFormat:@"[objc] smoke.py=%@\n", smokePath];

  Py_Initialize();

  wchar_t *arg0 = Py_DecodeLocale("SpacySmoke", NULL);
  wchar_t *pyargv[] = { arg0, NULL };
  if (arg0)
    PySys_SetArgv(1, pyargv);

  FILE *fp = fopen(smokePath.UTF8String, "r");
  if (!fp) {
    [out appendFormat:@"fopen failed for %@\n", smokePath];
    Py_Finalize();
    if (arg0)
      PyMem_RawFree(arg0);
    return out;
  }

  int rc = PyRun_SimpleFile(fp, smokePath.UTF8String);
  fclose(fp);
  Py_Finalize();
  if (arg0)
    PyMem_RawFree(arg0);

  [out appendFormat:@"[objc] PyRun_SimpleFile exit code %d\n", rc];

  NSString *logFile = [docs stringByAppendingPathComponent:@"spacy_smoke_log.txt"];
  NSError *err = nil;
  NSString *body = [NSString stringWithContentsOfFile:logFile encoding:NSUTF8StringEncoding error:&err];
  if (body.length > 0) {
    [out appendString:@"\n--- spacy_smoke_log.txt ---\n"];
    [out appendString:body];
  } else {
    [out appendFormat:@"\n(no log at %@: %@)\n", logFile, err.localizedDescription ?: @"empty");
  }

  return out;
}

- (void)onRun {
  self.textView.text = @"Running embedded Python…\n";
  NSString *res = [[NSBundle mainBundle] resourcePath];
  NSString *smoke = [[NSBundle mainBundle] pathForResource:@"smoke" ofType:@"py"];
  NSArray *docs = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES);

  __weak typeof(self) weakSelf = self;
  dispatch_async(dispatch_get_global_queue(QOS_CLASS_USER_INITIATED, 0), ^{
    NSString *txt = RunEmbeddedPython(docs, res, smoke);
    typeof(self) strong = weakSelf;
    if (!strong)
      return;
    strong.lastLogPath = [docs.firstObject stringByAppendingPathComponent:@"spacy_smoke_log.txt"];
    dispatch_async(dispatch_get_main_queue(), ^{
      strong.textView.text = txt;
    });
  });
}

- (void)onCopy {
  NSString *t = self.textView.text ?: @"";
  if (t.length == 0)
    return;
  [UIPasteboard generalPasteboard].string = t;
  UIAlertController *a = [UIAlertController alertControllerWithTitle:@"Copied" message:@"Log text is on the pasteboard." preferredStyle:UIAlertControllerStyleAlert];
  [a addAction:[UIAlertAction actionWithTitle:@"OK" style:UIAlertActionStyleDefault handler:nil]];
  [self presentViewController:a animated:YES completion:nil];
}

- (void)onShare {
  NSString *p = self.lastLogPath;
  if (p.length == 0)
    p = [NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES).firstObject stringByAppendingPathComponent:@"spacy_smoke_log.txt"];
  if (![[NSFileManager defaultManager] isReadableFileAtPath:p]) {
    UIAlertController *a = [UIAlertController alertControllerWithTitle:@"No log file" message:p preferredStyle:UIAlertControllerStyleAlert];
    [a addAction:[UIAlertAction actionWithTitle:@"OK" style:UIAlertActionStyleDefault handler:nil]];
    [self presentViewController:a animated:YES completion:nil];
    return;
  }
  NSURL *url = [NSURL fileURLWithPath:p isDirectory:NO];
  UIActivityViewController *av = [[UIActivityViewController alloc] initWithActivityItems:@[ url ] applicationActivities:nil];
  av.popoverPresentationController.sourceView = self.view;
  av.popoverPresentationController.sourceRect = CGRectMake(CGRectGetMidX(self.view.bounds), CGRectGetMidY(self.view.bounds), 0, 0);
  [self presentViewController:av animated:YES completion:nil];
}
@end

@interface AppDelegate : UIResponder <UIApplicationDelegate>
@property (nonatomic, strong) UIWindow *window;
@end

@implementation AppDelegate

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
  self.window = [[UIWindow alloc] initWithFrame:[UIScreen mainScreen].bounds];
  SpacySmokeVC *root = [[SpacySmokeVC alloc] init];
  UINavigationController *nav = [[UINavigationController alloc] initWithRootViewController:root];
  self.window.rootViewController = nav;
  [self.window makeKeyAndVisible];
  return YES;
}
@end

int main(int argc, char *argv[]) {
  @autoreleasepool {
    return UIApplicationMain(argc, argv, nil, NSStringFromClass([AppDelegate class]));
  }
}
